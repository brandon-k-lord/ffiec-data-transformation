from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from ..constants import connections


class SessionHandler:
    """
    A class that provides methods for creating and managing PostgreSQL database sessions.
    It supports both synchronous and asynchronous session management, as well as a singleton pattern
    for engine reuse.

    Attributes:
        _postgres_engine (Engine or None): A cached synchronous engine for PostgreSQL connection.
        _postgres_async_engine (AsyncEngine or None): A cached asynchronous engine for PostgreSQL connection.
        _postgres_connection (str): The connection URL for the PostgreSQL database, typically from constants.
    """

    _postgres_engine: Engine = None
    _postgres_async_engine: AsyncEngine = None
    _postgres_connection: str = connections.POSTGRES_CONNECTION

    @classmethod
    def create_postgres_engine(cls) -> Engine:
        """
        Creates a new synchronous engine for connecting to PostgreSQL.

        This method does not cache the created engine, so every call will result in a new engine instance.
        Useful when a new connection is required for each call.

        Returns:
            Engine: A new SQLAlchemy engine for PostgreSQL.
        """
        return create_engine(url=cls._postgres_connection, echo=False)

    @classmethod
    def create_postgres_async_engine(cls) -> AsyncEngine:
        """
        Creates a new asynchronous engine for connecting to PostgreSQL.

        This method does not cache the created engine, so every call will result in a new engine instance.
        Useful for asynchronous operations that require a fresh engine.

        Returns:
            AsyncEngine: A new asynchronous SQLAlchemy engine for PostgreSQL.
        """
        return create_async_engine(cls._postgres_connection, echo=True)

    @classmethod
    def get_postgres_engine(cls) -> Engine:
        """
        Retrieves the singleton synchronous PostgreSQL engine.

        This method will return a cached instance of the engine if one already exists,
        or it will create and cache a new engine if none exists.

        Returns:
            Engine: A cached or newly created synchronous SQLAlchemy engine for PostgreSQL.
        """
        if cls._postgres_engine is None:
            cls._postgres_engine = create_engine(
                url=cls._postgres_connection, echo=False
            )
        return cls._postgres_engine

    @classmethod
    def get_postgres_async_engine(cls) -> AsyncEngine:
        """
        Retrieves the singleton asynchronous PostgreSQL engine.

        This method will return a cached instance of the engine if one already exists,
        or it will create and cache a new engine if none exists.

        Returns:
            AsyncEngine: A cached or newly created asynchronous SQLAlchemy engine for PostgreSQL.
        """
        if cls._postgres_async_engine is None:
            cls._postgres_async_engine = create_async_engine(
                cls._postgres_connection, echo=True
            )
        return cls._postgres_async_engine

    @classmethod
    def create_postgres_async_session_factory(cls) -> async_sessionmaker:
        """
        Creates a new asynchronous session factory bound to the asynchronous PostgreSQL engine.

        This session factory can be used to create sessions for asynchronous interactions with the database.

        Returns:
            sessionmaker: A factory function for creating asynchronous sessions bound to the PostgreSQL engine.
        """
        return async_sessionmaker(
            bind=cls.create_postgres_async_engine(),
            autoflush=False,
            expire_on_commit=False,
        )

    @classmethod
    def get_postgres_async_session_factory(cls) -> async_sessionmaker:
        """
        Retrieves the singleton asynchronous session factory bound to the cached asynchronous PostgreSQL engine.

        This method will return a cached session factory if one already exists, or it will create a new one
        based on the singleton engine.

        Returns:
            sessionmaker: A factory function for creating asynchronous sessions bound to the cached PostgreSQL engine.
        """
        return async_sessionmaker(
            bind=cls.get_postgres_async_engine(),
            autoflush=False,
            expire_on_commit=False,
        )
