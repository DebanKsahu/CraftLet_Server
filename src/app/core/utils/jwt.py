from typing import Any, Dict

import jwt

from app.config import settings


def createJwt(payload: Dict[str, Any]):
    return jwt.encode(
        payload=payload,
        key=settings.appSettings.JWT_SECRET_KEY,
        algorithm=settings.appSettings.JWT_ALGORITHM,
    )


def decodeJwt(token: str):
    return jwt.decode(
        jwt=token,
        key=settings.appSettings.JWT_SECRET_KEY,
        algorithms=[settings.appSettings.JWT_ALGORITHM],
    )
