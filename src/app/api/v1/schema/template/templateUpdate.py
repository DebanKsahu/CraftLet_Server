from typing import List

from pydantic import BaseModel
from pydantic.fields import Field


class TemplateUpdate(BaseModel):
    templateId: str = Field(min_length=1)
    addTags: List[str] | None = Field(default=None)
    removeTags: List[str] | None = Field(default=None)
    description: str | None = Field(default=None)
