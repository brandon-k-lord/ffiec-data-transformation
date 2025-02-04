from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..handlers.session import SessionHandler


async def get_postgres_async_db() -> AsyncGenerator[AsyncSession]:
    """
    Asynchronously retrieves a new database session from the session factory.

    This function creates a new async session factory using `SessionHandler.create_postgres_async_session_factory()`
    and provides an isolated session within the `async with` context. The session will be automatically closed
    after use.

    Yields:
        AsyncSession: An asynchronous database session that can be used to interact with the database.

    Example:
        async for db in get_postgres_async_db():
            # Use the db session here
            result = await db.execute(query)
    """
    LocalAsyncSession = SessionHandler.create_postgres_async_session_factory()
    async with LocalAsyncSession() as db:
        try:
            yield db
        finally:
            await db.close()


async def get_postgres_async_shared_db() -> AsyncGenerator[AsyncSession]:
    """
    Asynchronously retrieves a shared database session from the session factory.

    This function retrieves a shared async session factory using `SessionHandler.get_postgres_async_session_factory()`
    and provides the session within the `async with` context. The session will be automatically closed after use.
    The session can be reused across different parts of the application.

    Yields:
        AsyncSession: A shared asynchronous database session that can be used to interact with the database.

    Example:
        async for db in get_postgres_async_shared_db():
            # Use the shared db session here
            result = await db.execute(query)
    """
    LocalAsyncSession = SessionHandler.get_postgres_async_session_factory()
    async with LocalAsyncSession() as db:
        try:
            yield db
        finally:
            await db.close()
