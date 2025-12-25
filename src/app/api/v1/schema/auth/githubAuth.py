from pydantic import BaseModel, Field


class GithubUser(BaseModel):
    id: int
    login: str
    avatarUrl: str | None = Field(default=None)
    htmlUrl: str | None = Field(default=None)

class GithubEmail(BaseModel):
    email: str
    primary: bool
    verified: bool