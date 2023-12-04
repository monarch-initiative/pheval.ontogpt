from pathlib import Path

from pydantic import BaseModel, Field


class OntoGPTToolSpecificConfigurations(BaseModel):
    model: str = Field(...)
    template: Path = Field(...)
    constrained_list_path: Path = Field(None)
