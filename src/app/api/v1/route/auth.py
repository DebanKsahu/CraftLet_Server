from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.v1.dependency import getMongoDatabase
from app.api.v1.schema.auth.githubAuth import GithubEmail, GithubUser
from app.api.v1.schema.auth.token import Token
from app.config import settings
from app.core.client import createGithubClient
from app.core.decorator import public
from app.core.utils.jwt import createJwt
from app.db.model.user import UserInDb

authRouter = APIRouter(prefix="/api/v1/auth", tags=["Auth (V1)"])


@authRouter.get("/github/login/{frontendState}")
@public
async def githubLogin(request: Request, frontendState: str):
    redirectUrl = request.url_for("githubCallback")
    async with createGithubClient(
        redirectUrl=redirectUrl, scope="read:user user:email"
    ) as client:
        authUrl, state = client.create_authorization_url(
            url=settings.authSettings.githubAuthSettings.AUTHORIZE_URL
        )
        request.session["oauthServerState"] = state
        request.session["oauthFrontendState"] = frontendState
    return RedirectResponse(url=authUrl)


@authRouter.get("/github/callback")
@public
async def githubCallback(
    request: Request, mongoDatabase: AsyncIOMotorDatabase = Depends(getMongoDatabase)
):
    savedOauthState = request.session.get("oauthServerState", None)
    currentOAuthState = request.query_params.get("state", None)
    if (
        savedOauthState != currentOAuthState
        or (savedOauthState is None)
        or (currentOAuthState is None)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OAuth state. Possible CSRF attack or expired session.",
        )
    else:
        code = request.query_params.get("code")
        redirectUrl = request.url_for("githubCallback")
        async with createGithubClient(redirectUrl=redirectUrl) as client:
            accessToken = await client.fetch_token(
                url=settings.authSettings.githubAuthSettings.TOKEN_URL,
                code=code,
                grant_type="authorization_code",
                headers={"Accept": "application/json"},
            )

            userDetail = await client.get(
                url=settings.authSettings.githubAuthSettings.API_BASE + "user",
                headers={
                    "Authorization": f"Bearer {accessToken['access_token']}",
                    "Accept": "application/json",
                },
            )

            githubUser = GithubUser.model_validate(userDetail.json())

            emailDetails = await client.get(
                url=settings.authSettings.githubAuthSettings.API_BASE + "user/emails",
                headers={
                    "Authorization": f"Bearer {accessToken['access_token']}",
                    "Accept": "application/json",
                },
            )
            primaryEmail = None
            if emailDetails.status_code == 200:
                emails = [
                    GithubEmail.model_validate(emailDetail)
                    for emailDetail in emailDetails.json()
                ]
                primaryEmailDetail = next(
                    (email for email in emails if email.primary and email.verified),
                    None,
                )
                if primaryEmailDetail is None:
                    primaryEmail = emails[0].email
                else:
                    primaryEmail = primaryEmailDetail.email

        if primaryEmail is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="GitHub account does not have a verified email address.",
            )
        userCollection = mongoDatabase["users"]
        existUser = await userCollection.find_one({"githubId": githubUser.id})
        if existUser is None:
            newUser = UserInDb(
                email=primaryEmail,
                githubId=githubUser.id,
                githubUsername=githubUser.login,
                githubAvatarUrl=githubUser.avatarUrl,
                githubProfilePage=githubUser.htmlUrl,
            )
            newUserDict = newUser.model_dump(by_alias=True)
            await userCollection.insert_one(newUserDict)
        jwtPayload = {"id": githubUser.id}
        jwtToken = createJwt(payload=jwtPayload)
        return Token(token=jwtToken, type="Bearer")
