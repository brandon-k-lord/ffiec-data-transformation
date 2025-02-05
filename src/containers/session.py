"""
session

This module defines the `SessionContainer` class, which provides methods for creating
and managing PostgreSQL database sessions. It supports synchronous session management
while implementing a singleton pattern for engine reuse.

Dependencies:
    - `Engine`, `create_engine`: Synchronous database engine utilities from SQLAlchemy.
    - `Session`, `sessionmaker`: Synchronous session management utilities.
    - `connection`: Database connection constants from the constants module.

The `SessionContainer` class supports:
    - Creating new synchronous PostgreSQL engines.
    - Caching and reusing a singleton engine for synchronous connections.
    - Generating session factories for database interactions.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..constants import connection


class SessionContainer:
    """
    A container class for managing PostgreSQL database sessions.

    This class provides methods for:
    - Creating new synchronous PostgreSQL engines.
    - Caching and retrieving singleton instances of these engines.
    - Generating session factories for database operations.

    Attributes:
        _postgres_engine (Engine or None): Cached synchronous PostgreSQL engine.
        _postgres_connection (str): Database connection URL from constants.
    """

    _postgres_engine: Engine = None
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
    def create_postgres_session_factory(cls) -> sessionmaker:
        """
        Creates a new session factory bound to a fresh PostgreSQL engine.

        This method provides an independent session factory that does not reuse a cached engine.

        Returns:
            sessionmaker: A new session factory for PostgreSQL interactions.
        """
        return sessionmaker(
            bind=cls.create_postgres_engine(),
            autoflush=False,
            expire_on_commit=False,
        )

    @classmethod
    def get_postgres_session_factory(cls) -> sessionmaker:
        """
        Retrieves a session factory bound to the singleton PostgreSQL engine.

        This method ensures that all sessions use the same cached engine.

        Returns:
            sessionmaker: A session factory for PostgreSQL interactions.
        """
        return sessionmaker(
            bind=cls.get_postgres_engine(),
            autoflush=False,
            expire_on_commit=False,
        )

    @classmethod
    @contextmanager
    def get_postgres_db(cls) -> Generator[Session, None, None]:
        """
        Retrieves a new database session from the session factory.

        This function creates a new session factory using `SessionContainer.create_postgres_session_factory()`
        and provides an isolated session within the `with` context. The session will be automatically closed
        after use.

        Yields:
            Session: A synchronous database session that can be used to interact with the database.

        Example:
            with SessionContainer.get_postgres_db() as db:
                # Use the db session here
                result = db.execute(query)
        """
        LocalSession = cls.create_postgres_session_factory()
        with LocalSession() as db:
            try:
                yield db
            finally:
                db.close()

    @classmethod
    @contextmanager
    def get_postgres_shared_db(cls) -> Generator[Session, None, None]:
        """
        Retrieves a shared database session from the session factory.

        This function retrieves a shared session factory using `SessionContainer.get_postgres_session_factory()`
        and provides the session within the `with` context. The session will be automatically closed after use.
        The session can be reused across different parts of the application.

        Yields:
            Session: A shared synchronous database session that can be used to interact with the database.

        Example:
            with SessionContainer.get_postgres_shared_db() as db:
                # Use the shared db session here
                result = db.execute(query)
        """
        LocalSession = cls.get_postgres_session_factory()
        with LocalSession() as db:
            try:
                yield db
            finally:
                db.close()
