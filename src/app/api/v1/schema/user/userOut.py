from pydantic import BaseModel, Field


class UserOut(BaseModel):
    username: str = Field(min_length=1)
    githubProfile: str | None = Field(default=None)
    githubAvatarUrl: str | None = Field(default=None)
