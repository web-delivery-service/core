from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.settings.config import settings


class DatabaseManager:
    DATABASE_URL = settings.DB_URL
    DATABASE_PARAMS = {}

    def __init__(self):
        self.engine = create_async_engine(url=self.DATABASE_URL, **self.DATABASE_PARAMS)

        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False, autoflush=False, autocommit=False
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        session = self.session_factory()
        try:
            yield session
        finally:
            await session.close()


db_manager = DatabaseManager()
