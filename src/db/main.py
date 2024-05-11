from sqlmodel import create_engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from sqlmodel import SQLModel



engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))


async def initdb():
    """create a connection to our db"""
    
    async with engine.begin() as conn:
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)



async def get_session() -> AsyncSession:
    """Dependency to provide the session object"""
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session