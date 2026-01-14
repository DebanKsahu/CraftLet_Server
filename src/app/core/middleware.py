from fastapi import HTTPException, Request, status
from fastapi.routing import APIRoute

from app.core.enum import EndpointType
from app.core.utils.jwt import decodeJwt


class AuthRoute(APIRoute):
    def get_route_handler(self):
        originalHandler = super().get_route_handler()

        async def customHandler(request: Request):
            endpoint = self.endpoint
            if getattr(endpoint, "endpointType", EndpointType.PUBLIC):
                return await originalHandler(request)
            elif getattr(endpoint, "endpointType", EndpointType.PROTECTED):
                auth = request.headers.get("authorization")
                if not auth or not auth.startswith("Bearer "):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Missing or invalid Authorization header",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                token = auth.split(" ", 1)[1]
                try:
                    payload = decodeJwt(token=token)
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Could not validate credentials",
                    ) from e
                userId = payload.get("id", None)
                userName = payload.get("name", None)
                if userId is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token payload missing id",
                    )
                if userName is None:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token payload missing Name",
                    )
                request.state.userId = userId
                request.state.userName = userName
                return await originalHandler(request)
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Private endpoint — not currently accessible",
                )

        return customHandler
