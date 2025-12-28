from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class GithubAuthSettings(BaseModel):
    CLIENT_ID: str
    CLIENT_SECRET: str
    AUTHORIZE_URL: str
    TOKEN_URL: str
    API_BASE: str
    FINE_GRAINED_PAT: str


class AuthSettings(BaseModel):
    githubAuthSettings: GithubAuthSettings = Field(alias="github_auth_settings")


class MongoDbSettings(BaseModel):
    DB_URL: str
    DB_NAME: str
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_HOST: str
    APP_NAME: str

    @property
    def DB_URL(self):
        dbUrl = f"mongodb+srv://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/?appName={self.APP_NAME}"
        return dbUrl


class DbSettings(BaseModel):
    mongoDbSettings: MongoDbSettings = Field(alias="mongo_db_settings")

class AppSettings(BaseModel):
    SESSION_SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter=".",
        env_nested_max_split=3,
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )

    authSettings: AuthSettings = Field(alias="auth_settings")
    dbSettings: DbSettings = Field(alias="db_settings")
    appSettings: AppSettings = Field(alias="app_settings")

settings = Settings()

if __name__ == "__main__":
    print(settings)
