from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    openai_api_key: str
    chat_history_table: str = "chat_history"


settings = Settings()
