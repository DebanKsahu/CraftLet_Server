from typing import List

from pydantic.main import BaseModel


class TemplateOut(BaseModel):
    name: str
    tags: List[str]
    useCount: int
    version: str
    description: str
