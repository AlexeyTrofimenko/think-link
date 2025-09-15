from pydantic_settings import BaseSettings, SettingsConfigDict


class N8nSettings(BaseSettings):
    N8N_URL: str | None = None
    N8N_DISABLED: bool = False

    model_config = SettingsConfigDict(env_file=".envs/n8n.env", extra="ignore")


n8n_settings = N8nSettings()
