import json
from pathlib import Path

from pheval.post_processing.post_processing import PhEvalDiseaseResult, generate_pheval_result
from pheval.utils.file_utils import files_with_suffix


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
        return result["disease"]

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


def create_standardised_results(
    raw_results_dir: Path, output_dir: Path, sort_order: str = "descending"
) -> None:
    """Write standardised variant results from OntoGPT json output."""
    for result in files_with_suffix(raw_results_dir, ".json"):
        ontogpt_result = read_ontogpt_result(result)
        pheval_disease_result = PhEvalDiseaseResultFromOntoGPT(
            ontogpt_result
        ).extract_pheval_requirements()
        generate_pheval_result(
            pheval_disease_result, sort_order, output_dir, trim_ontogpt_result(result)
        )
