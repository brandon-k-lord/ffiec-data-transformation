"""
worker

This module defines the `WorkerContainer` class, which centralizes the execution of workers
in separate processes using process-based concurrency.
"""

from concurrent.futures import ProcessPoolExecutor

from sqlalchemy.orm import Session


from .imports import ImportContainer
from ..logger import logger
from .script import ScriptContainer
from .session import SessionContainer


class WorkerContainer:
    """
    Manages parallel execution of import and script tasks using process-based concurrency.

    This class acts as a container for handling data imports and script execution,
    utilizing `ProcessPoolExecutor` to execute tasks concurrently.

    Attributes:
        _import (ImportContainer): Handles data import operations.
        _script (ScriptContainer): Handles script execution.
    """

    def __init__(
        self,
        import_: ImportContainer,
        script: ScriptContainer,
        session: SessionContainer,
    ):
        """
        Initializes the WorkerContainer with import and script handling containers.

        Parameters:
            import_ (ImportContainer): Instance responsible for handling data imports.
            script (ScriptContainer): Instance responsible for executing scripts.
        """
        self._import: ImportContainer = import_
        self._script: ScriptContainer = script
        self._session: SessionContainer = session

    def dependency(self, db: Session):
        """
        Executes preflight and dependency scripts sequentially.

        This ensures that necessary scripts required for imports or other operations
        are executed before running workers.

        Parameters:
            db (Session): The database session used for script execution.
        """
        self._script.preflight_scripts(db=db)
        self._script.dependency_scripts(db=db)

    def safe_wrapper(self, func):
        """Creates a fresh DB engine inside each subprocess."""
        try:
            logger.info(f"Starting {func.__name__}")

            # Create a new engine inside the subprocess
            engine = self._session.create_postgres_engine()

            func(engine)  # Use the engine inside the subprocess
            logger.info(f"Completed {func.__name__}")

        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")

    def import_workers(self):
        """
        Executes import-related tasks concurrently using process-based concurrency.

        Parameters:
            engine (Engine): The SQLAlchemy engine used for database interactions.
        """

        with ProcessPoolExecutor() as exe:
            futures = [
                exe.submit(self.safe_wrapper, func)
                for func in [
                    self._import.attribute_import,
                    self._import.relationship_import,
                    self._import.transformation_import,
                    self._import.gov_identifier_import,
                    self._import.bhcf_import,
                ]
            ]

            for future in futures:
                future.result()

    def script_workers(self, db: Session):
        """
        Executes script-related tasks concurrently using process-based concurrency.

        The following script methods are executed in parallel:
            - attribute_scripts
            - relationship_scripts
            - transformation_scripts
            - gov_identifier_scripts
            - call_report_scripts

        Parameters:
            db (Session): The asynchronous database session used for script execution.
        """

        with ProcessPoolExecutor() as exe:
            futures = [
                exe.submit(self._script.attribute_scripts(db=db)),
                exe.submit(self._script.relationship_scripts(db=db)),
                exe.submit(self._script.transformation_scripts(db=db)),
                exe.submit(self._script.gov_identifier_scripts(db=db)),
                exe.submit(self._script.call_report_scripts(db=db)),
            ]
            for future in futures:
                future.result()
