from app.digitalAsset import digitalAssetRoute
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.route.auth import authRouter as authRouterV1
from app.config import settings
from app.db import closeMongo, configureCollections, connectMongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connectMongo()
    await configureCollections()
    yield
    await closeMongo()


app = FastAPI(title="CraftLet", lifespan=lifespan)

app.add_middleware(
    SessionMiddleware, secret_key=settings.appSettings.SESSION_SECRET_KEY
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authRouterV1)
app.include_router(digitalAssetRoute)
