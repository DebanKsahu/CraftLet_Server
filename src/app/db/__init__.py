from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING

from app.config import settings

mongoClient = None


async def connectMongo():
    global mongoClient

    mongoClient = AsyncIOMotorClient(
        settings.dbSettings.mongoDbSettings.DB_URL,
        maxPoolSize=16,
        minPoolSize=4,
    )
    await mongoClient.admin.command("ping")


async def closeMongo():
    global mongoClient
    if mongoClient is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MongoDB client is not initialized, can't close",
        )
    else:
        mongoClient.close()


async def configureCollections():
    if mongoClient is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MongoDB client is not initialized, can't configure the database",
        )
    else:
        database: AsyncIOMotorDatabase = mongoClient[
            settings.dbSettings.mongoDbSettings.DB_NAME
        ]
        userCollection = database.get_collection("users")
        await userCollection.create_index([("githubId", ASCENDING)], unique=True)
