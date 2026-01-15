from app.api.v1.schema.githubApi.repositoryDetail import RepositoryDetail
import httpx
from app.config import settings

GITHUB_API_VERSION_HEADER = "2022-11-28"
GITHUB_ACCEPT = "application/vnd.github+json"
BASE = "https://api.github.com"


async def getGithubRepoDetails(repoOwnerName: str, repoName: str):
    token = settings.apiSettings.githubApiSettings.FINE_GRAINED_PAT
    targetUrl = f"{BASE}/repos/{repoOwnerName}/{repoName}"

    headers = {
        "Accept": GITHUB_ACCEPT,
        "X-GitHub-Api-Version": GITHUB_API_VERSION_HEADER,
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient(timeout=3.0) as client:
        response = await client.get(targetUrl, headers=headers)
        response.raise_for_status()
    repoDetails = RepositoryDetail.model_validate(response.json())
    return repoDetails
