from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bot_token: str
    database_url: str = ""
    miniapp_url: str = ""
    timezone: str = "Asia/Tashkent"
    admin_id: int = 0  # Telegram user ID — faqat shu foydalanuvchi /yigish_* buyruqlarini ishlata oladi
    port: int = 8000  # Railway PORT — Mini App backend shu portda tinglaydi

    @field_validator("database_url")
    @classmethod
    def _asyncpg_uchun_toza_dsn(cls, v: str) -> str:
        # database_url asyncpg (scraper) tomonidan ham ishlatiladi — u
        # "postgresql+asyncpg://" yoki "postgres://" sxemasini tushunmaydi.
        # Qanday kelsa ham "postgresql://" ko'rinishiga keltiramiz.
        if v.startswith("postgresql+asyncpg://"):
            return "postgresql://" + v[len("postgresql+asyncpg://"):]
        if v.startswith("postgres://"):
            return "postgresql://" + v[len("postgres://"):]
        return v


settings = Settings()
