from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.utils.db.tables import BaseModel
from app.utils.config import get_config

URL = get_config()
engine = create_async_engine(URL, echo=True, future=True)


async def init_db(engine: AsyncEngine = engine, metadata=BaseModel.metadata):
    async with engine.begin() as session:
        await session.run_sync(metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=True)
    async with async_session() as session:
        yield session