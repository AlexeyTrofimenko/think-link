from pydantic_settings import BaseSettings, SettingsConfigDict


class OllamaSettings(BaseSettings):
    OLLAMA_URL: str | None = None
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text"
    OLLAMA_TIMEOUT_S: int = 60
    OLLAMA_DISABLED: bool = False

    model_config = SettingsConfigDict(env_file=".envs/ollama.env", extra="ignore")


ollama_settings = OllamaSettings()
