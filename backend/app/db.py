import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

#  DB URL 
DATABASE_URL = os.getenv("DATABASE_URL") 


# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Async DB dependency 
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session