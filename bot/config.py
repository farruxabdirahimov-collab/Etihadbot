from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bot_token: str
    database_url: str = ""
    miniapp_url: str = ""
    timezone: str = "Asia/Tashkent"


settings = Settings()
