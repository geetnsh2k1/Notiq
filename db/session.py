from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from db.setting import get_db_settings

settings = get_db_settings()
DATABASE_URL = settings.get_db_url()

engine = create_async_engine(
    DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=False,
    future=True,
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session
