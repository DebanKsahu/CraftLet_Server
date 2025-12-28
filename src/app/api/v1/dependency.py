from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

import app.db
from app.config import settings


def createMongoDatabase() -> AsyncIOMotorDatabase:
    if app.db.mongoClient is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MongoDB client is not initialized, Can't get database",
        )
    else:
        return app.db.mongoClient[settings.dbSettings.mongoDbSettings.DB_NAME]


def getMongoDatabase():
    database = createMongoDatabase()
    yield database
