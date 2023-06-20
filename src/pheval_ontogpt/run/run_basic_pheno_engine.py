import json
from pathlib import Path

from phenopackets import Phenopacket
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import phenopacket_reader

from pheval_ontogpt.prepare.clean_phenopacket import PhenopacketCleaner
from pheval_ontogpt.run.basic_pheno_engine import PhenoEngine


def run_phenopacket(pheno_engine: PhenoEngine, phenopacket: Phenopacket):
    """Run pheno engine on a single phenopacket."""
    return pheno_engine.predict_disease(phenopacket)


def write_json_result(
    ontogpt_result: [dict], raw_results_dir: Path, phenopacket_path: Path
) -> None:
    """Write the OntoGPT json output."""
    output_file = raw_results_dir.joinpath(f"{phenopacket_path.stem}-ontogpt_result.json")
    with open(output_file, "w") as outfile:
        json.dump(ontogpt_result, outfile, indent=4)
    outfile.close()


def run_phenopackets(phenopacket_dir: Path, raw_results_dir: Path) -> None:
    """Run a directory of phenopackets on the basic PhenoEngine."""
    pheno_engine = PhenoEngine()
    for phenopacket_path in all_files(phenopacket_dir):
        phenopacket = phenopacket_reader(phenopacket_path)
        clean_phenopacket = PhenopacketCleaner(phenopacket).clean_phenopacket()
        result = run_phenopacket(pheno_engine, clean_phenopacket)
        write_json_result(result, raw_results_dir, phenopacket_path)
