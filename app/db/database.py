from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db.config import db_settings

engine = create_async_engine(db_settings, echo=False)
session = async_sessionmaker(engine, expire_on_commit=False)
