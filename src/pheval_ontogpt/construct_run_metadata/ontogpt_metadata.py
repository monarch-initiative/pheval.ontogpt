from datetime import datetime
from dataclasses import dataclass


@dataclass
class OntoGPTMetaData:
    """Tool specific metadata."""
    api_call_date: datetime
    gpt_model: str
