from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.config import db_settings

engine = create_async_engine(db_settings.database_url_asyncpg, echo=False)
session = async_sessionmaker(engine, expire_on_commit=False)
