from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

ASYNC_DB_URL = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
