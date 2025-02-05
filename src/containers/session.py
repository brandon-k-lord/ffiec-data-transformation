"""
session

This module defines the `SessionContainer` class, which provides methods for creating
and managing PostgreSQL database sessions. It supports both synchronous and asynchronous
session management while implementing a singleton pattern for engine reuse.

Dependencies:
    - `Engine`, `create_engine`: Synchronous database engine utilities from SQLAlchemy.
    - `AsyncEngine`, `create_async_engine`, `async_sessionmaker`: Asynchronous database engine utilities.
    - `connection`: Database connection constants from the constants module.

The `SessionContainer` class supports:
    - Creating new synchronous and asynchronous PostgreSQL engines.
    - Caching and reusing a singleton engine for both synchronous and asynchronous connections.
    - Generating session factories for asynchronous interactions with the database.
"""

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

from ..constants import connection


class SessionContainer:
    """
    A container class for managing PostgreSQL database sessions.

    This class provides methods for:
    - Creating new synchronous and asynchronous PostgreSQL engines.
    - Caching and retrieving singleton instances of these engines.
    - Generating session factories for asynchronous database operations.

    Attributes:
        _postgres_engine (Engine or None): Cached synchronous PostgreSQL engine.
        _postgres_async_engine (AsyncEngine or None): Cached asynchronous PostgreSQL engine.
        _postgres_connection (str): Database connection URL from constants.
    """

    _postgres_engine: Engine = None
    _postgres_async_engine: AsyncEngine = None
    _postgres_connection: str = connection.POSTGRES_CONNECTION

    @classmethod
    def create_postgres_engine(cls) -> Engine:
        """
        Creates a new synchronous SQLAlchemy engine for PostgreSQL.

        This method returns a fresh engine instance each time it is called.

        Returns:
            Engine: A new synchronous SQLAlchemy engine for PostgreSQL.
        """
        return create_engine(url=cls._postgres_connection, echo=False)

    @classmethod
    def create_postgres_async_engine(cls) -> AsyncEngine:
        """
        Creates a new asynchronous SQLAlchemy engine for PostgreSQL.

        This method returns a fresh async engine instance each time it is called.

        Returns:
            AsyncEngine: A new asynchronous SQLAlchemy engine for PostgreSQL.
        """
        return create_async_engine(cls._postgres_connection, echo=True)

    @classmethod
    def get_postgres_engine(cls) -> Engine:
        """
        Retrieves or initializes the singleton synchronous PostgreSQL engine.

        If a cached engine instance exists, it is returned. Otherwise, a new engine
        is created and cached for reuse.

        Returns:
            Engine: A cached or newly created synchronous SQLAlchemy engine.
        """
        if cls._postgres_engine is None:
            cls._postgres_engine = create_engine(
                url=cls._postgres_connection, echo=False
            )
        return cls._postgres_engine

    @classmethod
    def get_postgres_async_engine(cls) -> AsyncEngine:
        """
        Retrieves or initializes the singleton asynchronous PostgreSQL engine.

        If a cached engine instance exists, it is returned. Otherwise, a new async engine
        is created and cached for reuse.

        Returns:
            AsyncEngine: A cached or newly created asynchronous SQLAlchemy engine.
        """
        if cls._postgres_async_engine is None:
            cls._postgres_async_engine = create_async_engine(
                cls._postgres_connection, echo=True
            )
        return cls._postgres_async_engine

    @classmethod
    def create_postgres_async_session_factory(cls) -> async_sessionmaker:
        """
        Creates a new asynchronous session factory bound to a fresh async PostgreSQL engine.

        This method provides an independent session factory that does not reuse a cached engine.

        Returns:
            async_sessionmaker: A new session factory for asynchronous PostgreSQL interactions.
        """
        return async_sessionmaker(
            bind=cls.create_postgres_async_engine(),
            autoflush=False,
            expire_on_commit=False,
        )

    @classmethod
    def get_postgres_async_session_factory(cls) -> async_sessionmaker:
        """
        Retrieves an asynchronous session factory bound to the singleton async PostgreSQL engine.

        This method ensures that all sessions use the same cached asynchronous engine.

        Returns:
            async_sessionmaker: A session factory for asynchronous PostgreSQL interactions.
        """
        return async_sessionmaker(
            bind=cls.get_postgres_async_engine(),
            autoflush=False,
            expire_on_commit=False,
        )
