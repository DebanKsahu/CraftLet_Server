from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette.responses import JSONResponse

from app.api.v1.dependency import getMongoDatabase
from app.api.v1.schema.template.templateFilter import TemplateFilter
from app.api.v1.schema.template.templateIn import TemplateIn
from app.api.v1.schema.template.templateOut import TemplateOut
from app.api.v1.schema.template.templatePage import TemplatePage
from app.api.v1.schema.template.templateUpdate import TemplateUpdate
from app.api.v1.service.templateService import (
    createNewTemplate,
    deleteExistingTemplate,
    getExistingTemplateDetail,
    handleTemplateList,
    updateExistingTemplate,
)
from app.core.decorator import protected
from app.core.middleware import AuthRoute

templateRouter = APIRouter(
    prefix="/api/v1/template", tags=["Template Management (V1)"], route_class=AuthRoute
)


@templateRouter.post("/", response_model=TemplatePage)
@protected
async def getTemplateList(
    templateFilter: TemplateFilter,
    mongoDatabase: AsyncIOMotorDatabase = Depends(getMongoDatabase),
    cursor: str | None = None,
):
    serviceResponse = await handleTemplateList(
        templateFilter=templateFilter, mongoDatabase=mongoDatabase, cursor=cursor, limit=50
    )
    return serviceResponse


@templateRouter.post("/createTemplate")
@protected
async def createTemplate(
    templateData: TemplateIn,
    request: Request,
    mongoDatabase: AsyncIOMotorDatabase = Depends(getMongoDatabase),
):
    userId: str = str(request.state.userId)
    userName: str = str(request.state.userName)
    await createNewTemplate(
        templateData=templateData, userId=userId, userName=userName, mongoDatabase=mongoDatabase
    )
    return JSONResponse(content={"message": "Template Successfully Created"}, status_code=200)


@templateRouter.patch("/updateTemplate")
@protected
async def updateTemplate(
    newFieldData: TemplateUpdate,
    request: Request,
    mongoDatabase: AsyncIOMotorDatabase = Depends(getMongoDatabase),
):
    documentModified = await updateExistingTemplate(newFieldData=newFieldData, mongoDatabase=mongoDatabase)
    return JSONResponse(content={"message": f"{documentModified} document modified"}, status_code=200)


@templateRouter.delete("/deleteTemplate")
@protected
async def deleteTemplate(
    templateId: str, request: Request, mongoDatabase: AsyncIOMotorDatabase = Depends(getMongoDatabase)
):
    documentDeleted = await deleteExistingTemplate(
        templateId=ObjectId(templateId), mongoDatabase=mongoDatabase
    )
    return JSONResponse(content={"message": f"{documentDeleted} document(s) deleted"}, status_code=200)


@templateRouter.get("/templateDetail", response_model=TemplateOut)
@protected
async def getTemplateDetail(
    templateId: str, request: Request, mongoDatabase: AsyncIOMotorDatabase = Depends(getMongoDatabase)
):
    templateDetail = await getExistingTemplateDetail(
        templateId=ObjectId(templateId), mongoDatabase=mongoDatabase
    )
    return templateDetail
