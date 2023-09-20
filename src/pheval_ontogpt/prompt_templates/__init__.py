from pathlib import Path

PHENOPACKET_PROMPT_DIR_PATH = Path(__file__).parent
JOINT_PHENOPACKET_PROMPT = PHENOPACKET_PROMPT_DIR_PATH / "joint_request_template.jinja2"
GENE_PHENOPACKET_PROMPT = PHENOPACKET_PROMPT_DIR_PATH / "gene_request_template.jinja2"
DISEASE_PHENOPACKET_PROMPT = PHENOPACKET_PROMPT_DIR_PATH / "disease_request_template.jinja2"
