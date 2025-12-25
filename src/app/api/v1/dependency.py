from motor.motor_asyncio import AsyncIOMotorDatabase

from app.config import settings
from app.db import mongoClient


def createMongoDatabase() -> AsyncIOMotorDatabase:
    if mongoClient is None:
        raise
    else:
        return mongoClient[settings.dbSettings.mongoDbSettings.DB_NAME]


def getMongoDatabase():
    database = createMongoDatabase()
    yield database
