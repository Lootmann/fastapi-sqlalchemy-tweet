from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#               postgresql+asyncpg://<db_username>:<db_secret>@<db_host>:<db_port>/<db_name>
ASYNC_DB_URL = "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)

# TODO: which do I use sessionmaerk or async_sessionmaker? Both are also fine.
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
