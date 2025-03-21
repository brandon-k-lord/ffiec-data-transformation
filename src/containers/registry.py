"""
registry module

This module defines the `RegistryContainer` class, which serves as a centralized 
process registry for managing worker processes, database sessions, schema management, 
and task execution.

It integrates with the following containers:
- `WorkerContainer`: Handles import and script execution workflows.
- `SessionContainer`: Manages database session creation.
- `SchemaContainer`: Facilitates schema-related operations, such as transformation schema creation.

The module ensures proper coordination between workers, session management, and 
asynchronous PostgreSQL database connections, enabling efficient task execution.
"""

from .schema import SchemaContainer
from .session import SessionContainer
from .worker import WorkerContainer


class RegistryContainer:
    """
    A centralized registry for managing and executing worker processes.

    This class orchestrates dependencies, database operations, schema management,
    import workflows, and script execution by coordinating with `WorkerContainer`,
    `SessionContainer`, and `SchemaContainer`.

    Attributes:
        _worker (WorkerContainer): Manages import workflows and script execution.
        _session (SessionContainer): Handles database session creation.
        _schema (SchemaContainer): Manages schema-related operations.
    """

    def __init__(
        self,
        worker: WorkerContainer,
        session: SessionContainer,
        schema: SchemaContainer,
    ) -> None:
        """
        Initializes the RegistryContainer with worker, session, and schema dependencies.

        Args:
            worker (WorkerContainer): Handles import and script execution tasks.
            session (SessionContainer): Manages database session creation.
            schema (SchemaContainer): Handles schema-related operations.
        """
        self._worker: WorkerContainer = worker
        self._session: SessionContainer = session
        self._schema: SchemaContainer = schema

    def process(self) -> None:
        """
        Executes the complete process pipeline.

        This method:
        1. Sets up dependencies using a shared PostgreSQL database connection.
        2. Triggers import tasks using a new PostgreSQL engine session.
        3. Executes script-based worker tasks using a separate PostgreSQL database connection.

        The workflow ensures that all required dependencies are initialized before
        executing imports and scripts.
        """
        with self._session.get_postgres_shared_db() as shared_db:
            self._worker.dependency(db=shared_db)

        self._worker.import_workers()

        with self._session.get_postgres_db() as db:
            self._worker.script_workers(db=db)

    def create_schema(self) -> None:
        """
        Initiates schema creation.
        """
        with self._session.get_postgres_shared_db() as db:
            self._schema.create_transformation_schema(db=db)
