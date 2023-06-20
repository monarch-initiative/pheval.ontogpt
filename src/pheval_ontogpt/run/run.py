from pathlib import Path

from pheval_ontogpt.run.run_basic_pheno_engine import run_phenopackets


def run_basic(testdata_dir: Path, raw_results_dir: Path):
    phenopacket_dir = testdata_dir.joinpath("phenopackets")
    run_phenopackets(phenopacket_dir, raw_results_dir)
