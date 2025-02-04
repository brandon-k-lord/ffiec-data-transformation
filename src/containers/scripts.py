from sqlalchemy.ext.asyncio import AsyncSession

from ..handlers import ScriptHandler
from .configs import ConfigContainer


class ScriptContainer:
    def __init__(self, config: ConfigContainer, script_handler: ScriptHandler):
        self._config: ConfigContainer = config
        self._script_handler: ScriptHandler = script_handler

    async def preflight_scripts(self, db: AsyncSession) -> None:
        """
        Executes the preflight script import process.
        Uses the configurations provided by `preflight_scripts` from the config container.
        """
        return await self._script_handler.execute_scripts(
            db=db,
            configs=self._config.preflight_scripts(),
        )

    async def dependency_scripts(self, db: AsyncSession) -> None:
        """
        Executes the dependency script import process.
        Uses the configurations provided by `dependency_scripts` from the config container.
        """
        return await self._script_handler.execute_scripts(
            db=db,
            configs=self._config.dependency_scripts(),
        )

    async def attribute_scripts(self, db: AsyncSession) -> None:
        """
        Executes the attribute script import process.
        Uses the configurations provided by `attribute_scripts` from the config container.
        """
        return await self._script_handler.execute_scripts(
            db=db,
            configs=self._config.attribute_scripts(),
        )

    async def relationship_scripts(self, db: AsyncSession) -> None:
        """
        Executes the relationship script import process.
        Uses the configurations provided by `relationship_scripts` from the config container.
        """
        return await self._script_handler.execute_scripts(
            db=db,
            configs=self._config.relationship_scripts(),
        )

    async def transformation_scripts(self, db: AsyncSession) -> None:
        """
        Executes the transformation script import process.
        Uses the configurations provided by `transformation_scripts` from the config container.
        """
        return await self._script_handler.execute_scripts(
            db=db,
            configs=self._config.transformation_scripts(),
        )

    async def gov_identifier_scripts(self, db: AsyncSession) -> None:
        """
        Executes the gov_identifier script import process.
        Uses the configurations provided by `gov_identifier_scripts` from the config container.
        """
        return await self._script_handler.execute_scripts(
            db=db,
            configs=self._config.gov_identifier_scripts(),
        )

    async def call_report_scripts(self, db: AsyncSession) -> None:
        """
        Executes the call_report script import process.
        Uses the configurations provided by `call_report_scripts` from the config container.
        """
        return await self._script_handler.execute_scripts(
            db=db,
            configs=self._config.call_report_scripts(),
        )
