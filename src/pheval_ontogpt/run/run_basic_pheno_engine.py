import json
from pathlib import Path

from phenopackets import Phenopacket
from pheval.utils.file_utils import all_files
from pheval.utils.phenopacket_utils import phenopacket_reader

from pheval_ontogpt.prepare.clean_phenopacket import PhenopacketCleaner
from pheval_ontogpt.run.basic_pheno_engine import PhenoEngine


def run_phenopacket(
    pheno_engine: PhenoEngine,
    phenopacket: Phenopacket,
    prompt_template: Path,
    constrained_list_path: Path = None,
):
    """Run pheno engine on a single phenopacket."""
    if constrained_list_path is not None:
        with open(constrained_list_path, "r") as f:
            constrained_list = f.readlines()
        f.close()
    else:
        constrained_list = None
    return pheno_engine.predict(phenopacket, prompt_template, constrained_list)
    # if gene_analysis and disease_analysis:
    #     return pheno_engine.predict(phenopacket, JOINT_PHENOPACKET_PROMPT)
    # elif gene_analysis:
    #     return pheno_engine.predict(phenopacket, GENE_PHENOPACKET_PROMPT)
    # elif disease_analysis:
    #     return pheno_engine.predict(phenopacket, DISEASE_PHENOPACKET_PROMPT)


def write_json_result(
    ontogpt_result: [dict], raw_results_dir: Path, phenopacket_path: Path
) -> None:
    """Write the OntoGPT json output."""
    output_file = raw_results_dir.joinpath(f"{phenopacket_path.stem}-ontogpt_result.json")
    with open(output_file, "w") as outfile:
        json.dump(ontogpt_result, outfile, indent=4)
    outfile.close()


def run_phenopackets(
    phenopacket_dir: Path,
    raw_results_dir: Path,
    model: str,
    prompt: Path,
    constrained_list_path: Path = None,
) -> None:
    """Run a directory of phenopackets on the basic PhenoEngine."""
    pheno_engine = PhenoEngine(model=model)
    for phenopacket_path in all_files(phenopacket_dir):
        phenopacket = phenopacket_reader(phenopacket_path)
        clean_phenopacket = PhenopacketCleaner(phenopacket).clean_phenopacket()
        result = run_phenopacket(pheno_engine, clean_phenopacket, prompt, constrained_list_path)
        write_json_result(result, raw_results_dir, phenopacket_path)
