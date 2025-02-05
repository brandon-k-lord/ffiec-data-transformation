"""
worker

This module defines the `WorkerContainer` class, which centralizes the execution of workers
in separate processes using process-based concurrency.
"""

from concurrent.futures import ProcessPoolExecutor

from sqlalchemy import Engine
from sqlalchemy.orm import Session


from .imports import ImportContainer
from .script import ScriptContainer


class WorkerContainer:
    """
    Manages parallel execution of import and script tasks using process-based concurrency.

    This class acts as a container for handling data imports and script execution,
    utilizing `ProcessPoolExecutor` to execute tasks concurrently.

    Attributes:
        _import (ImportContainer): Handles data import operations.
        _script (ScriptContainer): Handles script execution.
    """

    def __init__(self, import_: ImportContainer, script: ScriptContainer):
        """
        Initializes the WorkerContainer with import and script handling containers.

        Parameters:
            import_ (ImportContainer): Instance responsible for handling data imports.
            script (ScriptContainer): Instance responsible for executing scripts.
        """
        self._import: ImportContainer = import_
        self._script: ScriptContainer = script

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

    def import_workers(self, engine: Engine):
        """
        Executes import-related tasks concurrently using process-based concurrency.

        The following import methods are executed in parallel:
            - attribute_import
            - relationship_import
            - transformation_import
            - gov_identifier_import
            - bhcf_import

        Parameters:
            engine (Engine): The SQLAlchemy engine used for database interactions.
        """
        # with ProcessPoolExecutor() as executor:
        #     executor.map(
        #         lambda func, engine=engine: func(engine),
        #         [
        #             self._import.attribute_import,
        #             self._import.relationship_import,
        #             self._import.transformation_import,
        #             self._import.gov_identifier_import,
        #             self._import.bhcf_import,
        #         ],
        #     )

        self._import.attribute_import(engine=engine),
        self._import.relationship_import(engine=engine),
        self._import.transformation_import(engine=engine),
        self._import.gov_identifier_import(engine=engine),
        self._import.bhcf_import(engine=engine),

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
        # with ProcessPoolExecutor() as executor:
        #     executor.map(
        #         lambda func, db=db: func(db),
        #         [
        #             self._script.attribute_scripts,
        #             self._script.relationship_scripts,
        #             self._script.transformation_scripts,
        #             self._script.gov_identifier_scripts,
        #             self._script.call_report_scripts,
        #         ],
        #     )

        self._script.attribute_scripts(db=db),
        self._script.relationship_scripts(db=db),
        self._script.transformation_scripts(db=db),
        self._script.gov_identifier_scripts(db=db),
        self._script.call_report_scripts(db=db),
