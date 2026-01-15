from bson import ObjectId
from pydantic import BaseModel, Field

from app.db.model.customTypes import PyObjectId


class UserInDb(BaseModel):
    id: PyObjectId = Field(default_factory = ObjectId, alias="_id")
    email: str = Field(min_length=1)
    githubId: int
    githubUsername: str = Field(min_length=1)
    githubAvatarUrl: str | None = Field(default=None)
    githubProfilePage: str | None = Field(default=None)

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
    }
