from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str | None = None
    DB_PASS_FILE: str = "/run/secrets/pg_password"

    model_config = SettingsConfigDict(env_file=".envs/postgres.env", extra="ignore")

    @property
    def database_url_asyncpg(self) -> str:
        pwd = self.DB_PASS
        if not pwd:
            p = Path(self.DB_PASS_FILE)
            if p.exists():
                pwd = p.read_text().strip()
            else:
                pwd = ""
        return f"postgresql+asyncpg://{self.DB_USER}:{pwd}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

db_settings = Settings()
print(db_settings.database_url_asyncpg)
