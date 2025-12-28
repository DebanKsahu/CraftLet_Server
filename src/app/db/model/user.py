from pydantic import BaseModel, Field

from app.db.model.customTypes import PyObjectId


class UserInDb(BaseModel):
    id: PyObjectId = Field(alias="_id")
    email: str = Field(min_length=1)
    githubUsername: str
    githubAvatarUrl: str | None = Field(default=None)
    githubProfilePage: str | None = Field(default=None)

    class config:
        arbitrary_types_allowed = True
