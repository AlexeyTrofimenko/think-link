from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_USER: str | None = None
    DB_NAME: str | None = None
    DB_PASS: str | None = None
    DB_PASS_FILE: str = "/run/secrets/pg_password"

    model_config = SettingsConfigDict(env_file=".envs/postgres.env", extra="ignore")

    @property
    def database_url_asyncpg(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if not self.DB_HOST or not self.DB_PORT or not self.DB_USER or not self.DB_NAME:
            raise ValueError("Database configuration is incomplete")
        pwd = self.DB_PASS
        if not pwd:
            p = Path(self.DB_PASS_FILE)
            if p.exists():
                pwd = p.read_text().strip()
            else:
                pwd = ""
        return f"postgresql+asyncpg://{self.DB_USER}:{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


db_settings = Settings()
