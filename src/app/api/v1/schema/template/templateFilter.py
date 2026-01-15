from typing import List

from pydantic import BaseModel, Field


class TemplateFilter(BaseModel):
    templateNamePrefix: str | None = Field(default=None)
    templateAuthorNamePrefix: str | None = Field(default=None)
    templateTags: List[str] | None = Field(default=None)
