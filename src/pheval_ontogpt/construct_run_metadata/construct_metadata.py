from pheval.run_metadata import BasicOutputRunMetaData
from datetime import datetime

from pheval_ontogpt.construct_run_metadata.ontogpt_metadata import OntoGPTMetaData


def construct_run_metadata(metadata: BasicOutputRunMetaData, model: str) -> BasicOutputRunMetaData:
    """Add tool specific metadata to basic run metadata,"""
    metadata.tool_specific_configuration_options = OntoGPTMetaData(api_call_date=datetime.now(),
                                                                   gpt_model=model)
    return metadata