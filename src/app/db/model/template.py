from datetime import datetime, timezone
from typing import List

from bson.objectid import ObjectId
from pydantic import BaseModel, Field

from app.db.model.customTypes import PyObjectId


class TemplateInDb(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    authorId: str
    name: str = Field(min_length=1)
    authorName: str = Field(min_length=1)
    originalLink: str = Field(min_length=1)
    description: str | None = Field(default=None)
    version: str = Field(default="0.1.0")
    useCount: int = Field(default=0)
    tags: List[str] = Field(default_factory=list)
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
    }
