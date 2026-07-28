from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from bot.config import settings

# settings.database_url — asyncpg (scraper) uchun ham ishlatiladigan xom
# postgresql:// DSN. SQLAlchemy async drayveri uchun sxemani almashtiramiz.
_sqlalchemy_dsn = settings.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine: AsyncEngine = create_async_engine(_sqlalchemy_dsn, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)
