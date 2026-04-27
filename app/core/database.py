import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

logger = logging.getLogger(__name__)

# Global variables for database
engine: object | None = None
async_session: async_sessionmaker[AsyncSession] | None = None

class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""
    pass


async def init_database():
    """Initialize the database connection."""
    global engine, async_session

    if not settings.database_url:
        logger.info("No Database URL found, skipping database initialization")
        return
    try:
        engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            pool_pre_ping=True,
            pool_recycle=300,
        )

        async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

async def get_database() -> AsyncSession:
    """Get a database session."""
    if not async_session:
        raise RuntimeError("Database not initialized")
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def check_database_health() -> bool:
    """Check the database health."""
    if not engine:
        return False

    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            return True
    except Exception:
        logger.error("DB health check failed.", exc_info=True)
        return False


