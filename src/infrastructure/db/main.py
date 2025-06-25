from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import settings
from src.infrastructure.db.base import Base

engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True
)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await engine.dispose()


async def get_session() -> AsyncSession:
    return async_session()
    