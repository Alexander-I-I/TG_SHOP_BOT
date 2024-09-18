from config import load_db_config
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from DATABASE.models import Base


config = load_db_config()

engine = create_async_engine(config.db_config, echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)