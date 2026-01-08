from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.config import settings

digitalAssetRoute = APIRouter(tags=["DigitalAsset"])


@digitalAssetRoute.get("/.well-known/assetlinks.json")
async def getAndroidAssetLinks():
    response = [
        {
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {
                "namespace": "android_app",
                "package_name": "com.example.craftletkmp",
                "sha256_cert_fingerprints": [
                    settings.digitalAssetSettings.deeplinkSettings.androidFingerprint
                ],
            },
        },
        {
            "relation": ["delegate_permission/common.get_login_creds"],
            "target": {
                "namespace": "web",
                "site": "https://craftlet-server.onrender.com",
            },
        },
        {
            "relation": ["delegate_permission/common.get_login_creds"],
            "target": {
                "namespace": "android_app",
                "package_name": "com.example.craftletkmp",
                "sha256_cert_fingerprints": [
                    settings.digitalAssetSettings.deeplinkSettings.androidFingerprint
                ],
            },
        },
    ]
    return JSONResponse(content=response)
