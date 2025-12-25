from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings

app = FastAPI(title="CraftLet")

app.add_middleware(
    SessionMiddleware, secret_key=settings.appSettings.SESSION_SECRET_KEY
)
