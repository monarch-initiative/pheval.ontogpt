from pathlib import Path

from pheval_ontogpt.run.run_basic_pheno_engine import run_phenopackets


def run_basic(
    testdata_dir: Path, raw_results_dir: Path, model: str, prompt: Path, constrained_list_path: Path
):
    """Run basic pheno engine on a directory of phenopackets."""
    phenopacket_dir = testdata_dir.joinpath("phenopackets")
    run_phenopackets(phenopacket_dir, raw_results_dir, model, prompt, constrained_list_path)
