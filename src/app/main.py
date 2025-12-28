from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.route.auth import authRouter as authRouterV1
from app.config import settings

app = FastAPI(title="CraftLet")

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
