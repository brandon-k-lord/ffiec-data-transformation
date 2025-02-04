import asyncio
from concurrent.futures import ProcessPoolExecutor

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Engine

from .imports import ImportContainer
from .scripts import ScriptContainer


class WorkersContainer:
    """
    Manages parallel execution of import and script tasks using process-based concurrency.

    This class acts as a container for handling import and script execution, utilizing
    `ProcessPoolExecutor` to execute tasks concurrently.

    Attributes:
        _imports (ImportContainer): An instance responsible for handling data imports.
        _scripts (ScriptContainer): An instance responsible for executing scripts.
    """

    def __init__(self, imports: ImportContainer, scripts: ScriptContainer):
        """
        Initializes the WorkersContainer with import and script handling containers.

        Parameters:
            imports (ImportContainer): An instance of ImportContainer to handle data imports.
            scripts (ScriptContainer): An instance of ScriptContainer to handle script execution.
        """
        self._imports: ImportContainer = imports
        self._scripts: ScriptContainer = scripts

    def _run_async_func(self, func, db):

        return asyncio.run(func(db))

    async def dependency(self, db: AsyncSession):
        """
        Executes preflight and dependency scripts sequentially.

        This method ensures that necessary scripts required for imports or other operations
        are executed before running workers.
        """
        await self._scripts.preflight_scripts(db=db)
        await self._scripts.dependency_scripts(db=db)

    def import_workers(self, engine: Engine):
        """
        Executes import-related tasks concurrently.

        This method runs multiple import functions in parallel using a process pool, improving
        performance for large data operations.

        The following import methods are executed concurrently:
            - attribute_import
            - relationship_import
            - transformation_import
            - gov_identifier_import
            - bhcf_import
        """
        with ProcessPoolExecutor() as executor:
            executor.map(
                lambda func, engine=engine: func(engine),
                [
                    self._imports.attribute_import,
                    self._imports.relationship_import,
                    self._imports.transformation_import,
                    self._imports.gov_identifier_import,
                    self._imports.bhcf_import,
                ],
            )

    def script_workers(self, db: AsyncSession):
        """
        Executes script-related tasks concurrently.

        This method runs multiple script functions in parallel using a process pool, improving
        performance for computationally heavy scripts.

        The following script methods are executed concurrently:
            - attribute_scripts
            - relationship_scripts
            - transformation_scripts
            - gov_identifier_scripts
            - call_report_scripts
        """

        with ProcessPoolExecutor() as executor:
            executor.map(
                lambda func, db=db: self._run_async_func(func=func, db=db),
                [
                    self._scripts.attribute_scripts,
                    self._scripts.relationship_scripts,
                    self._scripts.transformation_scripts,
                    self._scripts.gov_identifier_scripts,
                    self._scripts.call_report_scripts,
                ],
            )
