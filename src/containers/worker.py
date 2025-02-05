"""
worker

This module defines the `WorkerContainer` class, which centralizes the execution of workers
in separate processes using process-based concurrency.
"""

import asyncio
from concurrent.futures import ProcessPoolExecutor

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncSession

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

    def _run_async_func(self, func, db: AsyncSession):
        """Runs an asynchronous function in a synchronous context."""
        return asyncio.run(func(db))

    async def dependency(self, db: AsyncSession):
        """
        Executes preflight and dependency scripts sequentially.

        This ensures that necessary scripts required for imports or other operations
        are executed before running workers.

        Parameters:
            db (AsyncSession): The database session used for script execution.
        """
        await self._script.preflight_scripts(db=db)
        await self._script.dependency_scripts(db=db)

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
        with ProcessPoolExecutor() as executor:
            executor.map(
                lambda func, engine=engine: func(engine),
                [
                    self._import.attribute_import,
                    self._import.relationship_import,
                    self._import.transformation_import,
                    self._import.gov_identifier_import,
                    self._import.bhcf_import,
                ],
            )

    def script_workers(self, db: AsyncSession):
        """
        Executes script-related tasks concurrently using process-based concurrency.

        The following script methods are executed in parallel:
            - attribute_scripts
            - relationship_scripts
            - transformation_scripts
            - gov_identifier_scripts
            - call_report_scripts

        Parameters:
            db (AsyncSession): The asynchronous database session used for script execution.
        """
        with ProcessPoolExecutor() as executor:
            executor.map(
                lambda func, db=db: self._run_async_func(func=func, db=db),
                [
                    self._script.attribute_scripts,
                    self._script.relationship_scripts,
                    self._script.transformation_scripts,
                    self._script.gov_identifier_scripts,
                    self._script.call_report_scripts,
                ],
            )
