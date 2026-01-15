from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class RepositoryDetail(BaseModel):
    id: str
    name: str
    repoLink: str = Field(alias="html_url")
    description: str | None = Field(default=None)
    isFork: bool = Field(alias="fork")
    forkCount: int = Field(alias="forks_count")
    createdAt: datetime = Field(alias="created_at")

    model_config = {
        "extra": "ignore"
    }

    @field_validator("id", mode = "before")
    @classmethod
    def castIntToStr(cls, value: int):
        return str(value)
