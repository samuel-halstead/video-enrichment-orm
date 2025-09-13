import logging

from pydantic import PostgresDsn, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    # Configuration
    LOCAL: bool = False
    LOG_DEBUG: bool = False

    # POSTGRESQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "video-enrichment"
    POSTGRES_USER: str = "video-enrichment"
    POSTGRES_PASSWORD: str = "video-enrichment"
    POSTGRES_CONNECTION_URL: str | PostgresDsn = (
        "postgresql://video-enrichment:video-enrichment@localhost:5432/video-enrichment"
    )
    POSTGRES_APP_NAME: str = ""

    # Batch operations
    BATCH_SIZE: int = 1000

    @model_validator(mode="after")
    def assemble_db_connection(self) -> "Settings":
        self.POSTGRES_CONNECTION_URL = PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=int(self.POSTGRES_PORT),
            path=self.POSTGRES_DB,
        ).unicode_string()

        return self


settings = Settings()


logging.basicConfig(level=logging.DEBUG if settings.LOG_DEBUG else logging.INFO)
logger = logging.getLogger(__name__)
