from motor.motor_asyncio import AsyncIOMotorDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings

mongoClient = None


async def connectMongo():
    global mongoClient

    mongoClient = AsyncIOMotorClient(
        settings.dbSettings.mongoDbSettings.DB_URL, maxPoolSize=16, minPoolSize=4
    )


async def closeMongo():
    global mongoClient
    if mongoClient is None:
        raise
    else:
        mongoClient.close()

async def configureCollections():
    if mongoClient is None:
        raise
    else:
        database: AsyncIOMotorDatabase = mongoClient[settings.dbSettings.mongoDbSettings.DB_NAME]
        userCollection = database["users"]