from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    FASTAPI_APP_HOST: str
    FASTAPI_APP_PORT: int

    SUBD: str
    BD_ENGINE: str

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_OUTER_PORT: int
    DB_NAME: str

    # S3_ACCESS_KEY: str
    # S3_PIVATE_KEY: str
    # S3_BUCKET_NAME: str
    # S3_BUCKET_NAME_GROUPS: str
    # S3_URL: str
    # S3_FILE_FORMAT: str

    # SMTP_HOST: str
    # SMTP_PORT: int
    # SMTP_USER: str
    # SMTP_PASSWORD: str

    # REDIS_PORT: int
    # REDIS_HOST: str
    # REDIS_PASSWORD: str
    # REDIS_USER: str

    @property
    def DB_URL(self):
        return f"{self.SUBD}+{self.BD_ENGINE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_OUTER_PORT}/{self.DB_NAME}"

    # @property
    # def REDIS_URI(self):
    #     return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


class AuthSettings(BaseSettings):
    pass
    # SECRET_KEY: str
    # ALGORITHM: str
    # ACCESS_TOKEN_EXPIRE_MINUTES: int
    # REFRESH_TOKEN_EXPIRE_MINUTES: int

    # REFRESH_COOKIE_KEY: str
    # COOKIE_DOMAIN: str

    # JWT_PRIVATE_KEY_PATH: Path = BASE_DIR / "auth" / "certs" / "jwt_privatekey.pem"
    # JWT_PUBLIC_KEY_PATH: Path = BASE_DIR / "auth" / "certs" / "jwt_publickey.pem"

    # model_config = SettingsConfigDict(
    #     case_sensitive=True, env_file=BASE_DIR / "auth" / ".env"
    # )


auth_settings = AuthSettings()
settings = Settings()
