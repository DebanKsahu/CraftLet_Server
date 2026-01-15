from typing import List

from pydantic.fields import Field
from pydantic.main import BaseModel


class TemplateIn(BaseModel):
    templateLink: str = Field(min_length=1)
    description: str | None = Field(default=None)
    tags: List[str] = Field(default_factory=list)
