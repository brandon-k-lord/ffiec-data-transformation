from sqlalchemy import Engine

from ..handlers import ScriptHandler
from .configs import ConfigContainer


class ScriptContainer:
    def __init__(
        self, config: ConfigContainer, engine: Engine, script_handler: ScriptHandler
    ):
        self._config: ConfigContainer = config
        self._engine: Engine = engine
        self._script_handler: ScriptHandler = script_handler

    def preflight_scripts(self) -> None:
        """
        Executes the preflight script import process.
        Uses the configurations provided by `preflight_scripts` from the config container.
        """
        return self._script_handler.execute_scripts(
            engine=self._engine,
            configs=self._config.preflight_scripts(),
        )

    def dependency_scripts(self) -> None:
        """
        Executes the dependency script import process.
        Uses the configurations provided by `dependency_scripts` from the config container.
        """
        return self._script_handler.execute_scripts(
            engine=self._engine,
            configs=self._config.dependency_scripts(),
        )

    def attribute_scripts(self) -> None:
        """
        Executes the attribute script import process.
        Uses the configurations provided by `attribute_scripts` from the config container.
        """
        return self._script_handler.execute_scripts(
            engine=self._engine,
            configs=self._config.attribute_scripts(),
        )

    def relationship_scripts(self) -> None:
        """
        Executes the relationship script import process.
        Uses the configurations provided by `relationship_scripts` from the config container.
        """
        return self._script_handler.execute_scripts(
            engine=self._engine,
            configs=self._config.relationship_scripts(),
        )

    def transformation_scripts(self) -> None:
        """
        Executes the transformation script import process.
        Uses the configurations provided by `transformation_scripts` from the config container.
        """
        return self._script_handler.execute_scripts(
            engine=self._engine,
            configs=self._config.transformation_scripts(),
        )

    def gov_identifier_scripts(self) -> None:
        """
        Executes the gov_identifier script import process.
        Uses the configurations provided by `gov_identifier_scripts` from the config container.
        """
        return self._script_handler.execute_scripts(
            engine=self._engine,
            configs=self._config.gov_identifier_scripts(),
        )

    def call_report_scripts(self) -> None:
        """
        Executes the call_report script import process.
        Uses the configurations provided by `call_report_scripts` from the config container.
        """
        return self._script_handler.execute_scripts(
            engine=self._engine,
            configs=self._config.call_report_scripts(),
        )
