from typing import List

from pydantic.fields import Field
from pydantic.main import BaseModel

from app.api.v1.schema.template.templateListElement import TemplateListElement


class TemplatePage(BaseModel):
    data: List[TemplateListElement] = Field(default_factory=list)
    nextCursor: str | None = Field(default=None)
    hasMore: bool = Field(default=True)
