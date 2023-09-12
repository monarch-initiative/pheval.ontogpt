import json
from pathlib import Path

import click
from pheval.post_processing.post_processing import (
    PhEvalDiseaseResult,
    PhEvalGeneResult,
    generate_pheval_result,
)
from pheval.utils.file_utils import files_with_suffix
from pheval.utils.phenopacket_utils import GeneIdentifierUpdater, create_hgnc_dict


def read_ontogpt_result(ontogpt_result_path: Path) -> [dict]:
    """Read .json OntoGPT result."""
    with open(ontogpt_result_path, "r") as result:
        parsed_result = json.load(result)
    result.close()
    return parsed_result


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


def create_empty_results_file(output_dir: Path, result: Path, file_type: str):
    trimmed_result = trim_ontogpt_result(result)
    new_filename = str(trimmed_result).replace(".json", f"-pheval_{file_type}_result.tsv")
    output_path = output_dir.joinpath(f"pheval_{file_type}_results/{new_filename}")
    open(output_path, "w").close()


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

    def handle_empty_results(result_file: Path):
        if disease_analysis:
            create_empty_results_file(output_dir, result_file, "disease")
        if gene_analysis:
            create_empty_results_file(output_dir, result_file, "gene")

    for ontogpt_result_file in files_with_suffix(raw_results_dir, ".json"):
        try:
            ontogpt_result = read_ontogpt_result(ontogpt_result_file)

            if len(ontogpt_result) == 0:
                handle_empty_results(ontogpt_result_file)

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

        except KeyError:
            handle_empty_results(ontogpt_result_file)


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
