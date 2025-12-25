from authlib.integrations.httpx_client import AsyncOAuth2Client
from starlette.datastructures import URL

from app.config import settings


def createGithubClient(redirectUrl: URL, scope: str | None = None):
    githubClient = AsyncOAuth2Client(
        client_id=settings.authSettings.githubAuthSettings.CLIENT_ID,
        client_secret=settings.authSettings.githubAuthSettings.CLIENT_SECRET,
        redirect_uri=redirectUrl,
        scope=scope,
    )

    return githubClient
