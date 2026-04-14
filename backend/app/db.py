import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# You can either hardcode your DB URL directly:
DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/mydb"

# Or read it from OS environment variables if you set it externally:
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@127.0.0.1:5432/mydb")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Async DB dependency (for FastAPI)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session