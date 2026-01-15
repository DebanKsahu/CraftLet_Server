from app.api.v1.schema.template.templateOut import TemplateOut
import base64
import json
import re
from datetime import datetime
from typing import Any, Dict
from urllib.parse import urlparse

from bson.objectid import ObjectId
from fastapi.exceptions import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.api.v1.schema.template.templateFilter import TemplateFilter
from app.api.v1.schema.template.templateIn import TemplateIn
from app.api.v1.schema.template.templateListElement import TemplateListElement
from app.api.v1.schema.template.templatePage import TemplatePage
from app.api.v1.schema.template.templateUpdate import TemplateUpdate
from app.api.v1.service.githubService import getGithubRepoDetails
from app.db.model.template import TemplateInDb


async def handleTemplateList(
    templateFilter: TemplateFilter,
    mongoDatabase: AsyncIOMotorDatabase,
    cursor: str | None,
    limit: int,
):
    finalTemplateFilter = templateFilter.model_dump(exclude_unset=True, exclude_none=True)
    templateCollection: AsyncIOMotorCollection = mongoDatabase["templates"]

    mongoDbQuery = createMongoFilterQuery(finalTemplateFilter)

    if cursor is not None:
        createdAt, templateId = decodeTemplateCursor(cursor)
        mongoDbQuery["$or"] = [
            {"createdAt": {"$lt": createdAt}},
            {"createdAt": createdAt, "_id": {"$lt": templateId}},
        ]

    templateCursor = (
        templateCollection.find(mongoDbQuery, projection={"large_blob": 0})
        .sort([("createdAt", -1), ("_id", -1)])
        .limit(limit + 1)
    )
    templates = await templateCursor.to_list(length=limit + 1)
    processedTemplates = [
        TemplateListElement(
            id=str(template.get("_id", "No Id")),
            name=template.get("name", "Name not Found"),
            tags=template.get("tags", ["Tag Not Found"]),
            useCount=template.get("useCount", 0),
            version=template.get("version", "0.0.0"),
            description=template.get("description", "No description"),
        )
        for template in templates
    ]

    hasMore = len(templates) == limit + 1
    nextCursor = (
        encodeTemplateCursor(
            createdAt=templates[-1].get("createdAt"),
            templateId=templates[-1].get("_id"),
        )
        if hasMore
        else None
    )
    return TemplatePage(data=processedTemplates, nextCursor=nextCursor, hasMore=hasMore)


async def createNewTemplate(
    templateData: TemplateIn, userId: str, userName: str, mongoDatabase: AsyncIOMotorDatabase
):
    templateCollection = mongoDatabase["templates"]
    templatePath = urlparse(templateData.templateLink).path.strip("/")
    repoOwnerName, repoName = templatePath.split("/")
    repoDetails = await getGithubRepoDetails(repoOwnerName=repoOwnerName, repoName=repoName)
    newTemplateDetails = TemplateInDb(
        name=repoName,
        authorId=userId,
        authorName=userName,
        originalLink=templateData.templateLink,
        description=repoDetails.description,
        useCount=repoDetails.forkCount,
        createdAt=repoDetails.createdAt,
    )

    await templateCollection.insert_one(newTemplateDetails.model_dump(by_alias=True))


async def updateExistingTemplate(newFieldData: TemplateUpdate, mongoDatabase: AsyncIOMotorDatabase):
    templateCollection: AsyncIOMotorCollection = mongoDatabase["templates"]
    updateQuery: Dict[str, Any] = {}
    if newFieldData.addTags is not None:
        for i in range(len(newFieldData.addTags)):
            newFieldData.addTags[i] = newFieldData.addTags[i].strip().lower()
        updateQuery["$addToSet"] = {"tags": {"$each": newFieldData.addTags}}
    if newFieldData.removeTags is not None:
        for i in range(len(newFieldData.removeTags)):
            newFieldData.removeTags[i] = newFieldData.removeTags[i].strip().lower()
        updateQuery["$pull"] = {"tags": {"$in": newFieldData.removeTags}}
    if newFieldData.description is not None:
        if "$set" not in updateQuery:
            updateQuery["$set"] = {}
        updateQuery["$set"]["description"] = newFieldData.description

    try:
        templateId = ObjectId(newFieldData.templateId)
        result = await templateCollection.update_one(filter={"_id": templateId}, update=updateQuery)
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Template Not Found")

    return result.matched_count


async def deleteExistingTemplate(templateId: ObjectId, mongoDatabase: AsyncIOMotorDatabase):
    templateCollection = mongoDatabase.get_collection("templates")
    result = await templateCollection.delete_one(filter={"_id": templateId})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Template Not Found")
    return result.deleted_count

async def getExistingTemplateDetail(templateId: ObjectId, mongoDatabase: AsyncIOMotorDatabase):
    templateCollection = mongoDatabase.get_collection("templates")
    result: TemplateOut | None = await templateCollection.find_one(filter={"_id": templateId})
    if result is None:
        raise HTTPException(status_code=404, detail="Template Not Found")
    return result


def encodeTemplateCursor(createdAt: datetime, templateId: ObjectId):
    payload = {"createdAt": createdAt.isoformat(), "_id": str(templateId)}
    return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()


def decodeTemplateCursor(cursor: str):
    rawJsonStr = base64.urlsafe_b64decode(cursor.encode()).decode()
    payload = json.loads(rawJsonStr)
    return datetime.fromisoformat(payload.get("createdAt")), ObjectId(payload.get("_id"))


def createMongoFilterQuery(templateFilters: Dict[str, Any]):
    mongoFilterQuery = {}

    for key, value in templateFilters.items():
        match key:
            case "templateNamePrefix":
                mongoFilterQuery["name"] = {"$regex": re.escape(value), "$options": "i"}
            case "templateTags":
                mongoFilterQuery["tags"] = {"$all": value}
            case "templateAuthorNamePrefix":
                mongoFilterQuery["authorName"] = {"$regex": re.escape(value), "$options": "i"}
            case _:
                pass
    return mongoFilterQuery
