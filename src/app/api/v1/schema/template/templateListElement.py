from typing import List

from pydantic.main import BaseModel


class TemplateListElement(BaseModel):
    id: str
    name: str
    tags: List[str]
    useCount: int
    version: str
    description: str