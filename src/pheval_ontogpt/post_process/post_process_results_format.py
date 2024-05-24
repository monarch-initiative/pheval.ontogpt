import json
from pathlib import Path
from typing import Dict, List, Union

import click
from pheval.post_processing.post_processing import (
    PhEvalDiseaseResult,
    PhEvalGeneResult,
    generate_pheval_result,
)
from pheval.utils.file_utils import files_with_suffix
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict


class CheckResultFormat:
    """
    Class to check the format of a parsed JSON result for required keys
    based on the type of analysis.

    Attributes:
        parsed_result (Union[str, List[str]]): The parsed JSON result.
        gene_analysis (bool): Flag to indicate if gene analysis keys are required.
        disease_analysis (bool): Flag to indicate if disease analysis keys are required.
    """

    def __init__(
        self, parsed_result: Union[Dict, List[str]], gene_analysis: bool, disease_analysis: bool
    ):
        """
        Initialise the CheckResultFormat class with parsed JSON result and analysis flags.
        """
        self.parsed_result = parsed_result
        self.gene_analysis = gene_analysis
        self.disease_analysis = disease_analysis

    def check_keys_in_dict_format_json(self) -> Union[Dict, None]:
        """
        Check for required keys in a dictionary format JSON result.

        Returns:
            Union[Dict, None]: The parsed result if required keys are present, otherwise None.
        """
        if self.gene_analysis and all(
            key in self.parsed_result for key in ["score", "gene_symbol"]
        ):
            return self.parsed_result
        elif self.disease_analysis and all(
            key in self.parsed_result for key in ["disease_name", "omim_disease_id", "score"]
        ):
            return self.parsed_result

    def check_keys_in_list_format_json(self) -> Union[List[Dict], None]:
        """
        Check for required keys in a list of dictionaries format JSON result.

        Returns:
            Union[List[Dict], None]: A list of dictionaries with required keys if any, otherwise None.
        """
        filtered_results = []
        for entry in self.parsed_result:
            if self.gene_analysis and all(key in entry for key in ["score", "gene_symbol"]):
                filtered_results.append(entry)
            elif self.disease_analysis and all(
                key in entry for key in ["disease_name", "omim_disease_id", "score"]
            ):
                filtered_results.append(entry)
        return filtered_results if filtered_results else None

    def check_result_format(self) -> Union[Dict, List[Dict], None]:
        """
        Determine the format of the parsed JSON result and check for required keys.

        Returns:
            Union[Dict, List[Dict], None]: The parsed result if required keys are present, otherwise None.
        """
        if isinstance(self.parsed_result, list):
            return self.check_keys_in_list_format_json()
        if isinstance(self.parsed_result, dict):
            return self.check_keys_in_dict_format_json()
        return None


def read_ontogpt_result(
    ontogpt_result_path: Path, gene_analysis: bool = False, disease_analysis: bool = False
) -> [dict]:
    """Read .json OntoGPT result."""
    with open(ontogpt_result_path, "r") as result:
        parsed_result = json.load(result)
    result.close()
    return CheckResultFormat(parsed_result, gene_analysis, disease_analysis).check_result_format()


def trim_ontogpt_result(ontogpt_result_path: Path) -> Path:
    """Trim -ontogpt_result from results filename."""
    return Path(str(ontogpt_result_path.name.replace("-ontogpt_result", "")))


class PhEvalDiseaseResultFromOntoGPT:
    def __init__(self, ontogpt_result: [dict]):
        self.ontogpt_result = ontogpt_result

    @staticmethod
    def obtain_score(result: dict) -> float:
        """Obtain score."""
        return result["score"]

    @staticmethod
    def obtain_disease_name(result: dict) -> str:
        """Obtain disease name."""
        return result["disease_name"]

    @staticmethod
    def obtain_omim_disease_id(result: dict) -> str:
        """Obtain omim disease ID."""
        return result["omim_disease_id"]

    def extract_pheval_requirements(self) -> [PhEvalDiseaseResult]:
        """Extract PhEval disease requirements."""
        pheval_disease_results = []
        for result in self.ontogpt_result:
            pheval_disease_results.append(
                PhEvalDiseaseResult(
                    disease_name=self.obtain_disease_name(result),
                    disease_identifier=self.obtain_omim_disease_id(result),
                    score=self.obtain_score(result),
                )
            )
        return pheval_disease_results


class PhEvalDiseaseResultFromOntoGPTMondo:
    def __init__(self, ontogpt_result: [dict]):
        self.ontogpt_result = ontogpt_result

    @staticmethod
    def obtain_score(result: dict) -> float:
        """Obtain score."""
        return result["score"]

    @staticmethod
    def obtain_omim_disease_id(result: dict) -> str:
        """Obtain omim disease ID."""
        return result["omim_disease_id"]

    @staticmethod
    def obtain_disease_name(result: dict) -> str:
        """Obtain disease name."""
        return result["disease_name"]

    @staticmethod
    def mondo_found(mondo_ids: []) -> bool:
        for mondo_id in mondo_ids:
            if mondo_id.startswith("MONDO"):
                return True

    def extract_pheval_requirements(self) -> [PhEvalDiseaseResult]:
        """Extract PhEval disease requirements."""
        pheval_disease_results = []
        for result in self.ontogpt_result:
            if self.mondo_found(result["disease_ids"]):
                for mondo_id in result["disease_ids"]:
                    pheval_disease_results.append(
                        PhEvalDiseaseResult(
                            disease_name=self.obtain_disease_name(result),
                            disease_identifier=mondo_id,
                            score=self.obtain_score(result),
                        )
                    )
            else:
                pheval_disease_results.append(
                    PhEvalDiseaseResult(
                        disease_name=self.obtain_disease_name(result),
                        disease_identifier=self.obtain_omim_disease_id(result),
                        score=self.obtain_score(result),
                    )
                )
        return pheval_disease_results


class PhEvalGeneResultFromOntoGPT:
    def __init__(self, ontogpt_result: [dict], gene_identifier_updator: GeneIdentifierUpdater):
        self.ontogpt_result = ontogpt_result
        self.gene_identifier_updator = gene_identifier_updator

    @staticmethod
    def obtain_score(result: dict) -> float:
        """Obtain score."""
        return result["score"]

    @staticmethod
    def obtain_gene_symbol(result: dict) -> str:
        """Obtain gene name."""
        return result["gene_symbol"]

    def obtain_gene_ensembl_id(self, result: dict) -> str:
        """Obtain omim disease ID."""
        return self.gene_identifier_updator.find_identifier(result["gene_symbol"])

    def extract_pheval_requirements(self) -> [PhEvalDiseaseResult]:
        """Extract PhEval disease requirements."""
        pheval_gene_results = []
        for result in self.ontogpt_result:
            pheval_gene_results.append(
                PhEvalGeneResult(
                    gene_symbol=self.obtain_gene_symbol(result),
                    gene_identifier=self.obtain_gene_ensembl_id(result),
                    score=self.obtain_score(result),
                )
            )
        return pheval_gene_results


def create_standardised_results(
    raw_results_dir: Path,
    output_dir: Path,
    gene_analysis: bool,
    disease_analysis: bool,
    sort_order: str = "descending",
) -> None:
    """Write standardised PhEval results from OntoGPT json output."""

    gene_identifier_updator = GeneIdentifierUpdater(
        hgnc_data=create_hgnc_dict(), gene_identifier="ensembl_id"
    )
    for ontogpt_result_file in files_with_suffix(raw_results_dir, ".json"):
        ontogpt_result = read_ontogpt_result(ontogpt_result_file, gene_analysis, disease_analysis)
        if not ontogpt_result:
            print(ontogpt_result_file)
            continue
        if disease_analysis:
            pheval_disease_result = PhEvalDiseaseResultFromOntoGPT(
                ontogpt_result
            ).extract_pheval_requirements()
            generate_pheval_result(
                pheval_disease_result,
                sort_order,
                output_dir,
                trim_ontogpt_result(ontogpt_result_file),
            )

        if gene_analysis:
            pheval_gene_result = PhEvalGeneResultFromOntoGPT(
                ontogpt_result, gene_identifier_updator
            ).extract_pheval_requirements()
            generate_pheval_result(
                pheval_gene_result,
                sort_order,
                output_dir,
                trim_ontogpt_result(ontogpt_result_file),
            )


@click.command("standardise")
@click.option(
    "--output-dir",
    "-o",
    required=True,
    metavar="PATH",
    help="Output directory for standardised results.",
    type=Path,
)
@click.option(
    "--raw-results-dir",
    "-R",
    required=True,
    metavar="DIRECTORY",
    help="Full path to Ontogpt results directory to be standardised.",
    type=Path,
)
@click.option(
    "--gene-analysis/--no-gene-analysis",
    default=False,
    required=False,
    type=bool,
    show_default=True,
    help="Specify analysis for gene prioritisation",
)
@click.option(
    "--disease-analysis/--no-disease-analysis",
    default=False,
    required=False,
    type=bool,
    show_default=True,
    help="Specify analysis for disease prioritisation",
)
def create_standardised_results_command(
    raw_results_dir: Path, output_dir: Path, gene_analysis: bool, disease_analysis: bool
):
    if disease_analysis:
        output_dir.joinpath("pheval_disease_results").mkdir(exist_ok=True)
    if gene_analysis:
        output_dir.joinpath("pheval_gene_results").mkdir(exist_ok=True)
    create_standardised_results(raw_results_dir, output_dir, gene_analysis, disease_analysis)
