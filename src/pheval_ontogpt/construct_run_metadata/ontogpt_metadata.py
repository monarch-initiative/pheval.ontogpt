from dataclasses import dataclass
from datetime import datetime


@dataclass
class OntoGPTMetaData:
    """Tool specific metadata."""

    api_call_date: datetime
    gpt_model: str
