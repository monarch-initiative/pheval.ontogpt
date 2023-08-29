from pydantic import BaseModel, Field


class OntoGPTToolSpecificConfigurations(BaseModel):
    model: str = Field(...)