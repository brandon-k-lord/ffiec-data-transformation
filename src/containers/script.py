"""
script

This module defines the `ScriptContainer` class, which acts as an orchestrator for executing
various SQL scripts for the ELT processes. It utilizes configurations provided by `ConfigContainer`
and executes scripts using `ScriptHandler`.
"""

from sqlalchemy.orm import Session  # Updated to use synchronous Session

from ..handlers import ScriptHandler
from .config import ConfigContainer


class ScriptContainer:
    """
    A container class responsible for executing various script import processes.

    This class manages different categories of scripts and executes them synchronously
    using the `ScriptHandler`. The configurations for each script type are provided
    by the `ConfigContainer`.

    Attributes:
        _config (ConfigContainer): Provides script execution configurations.
        _script_handler (ScriptHandler): Executes scripts using the provided configurations.
    """

    def __init__(self, config: ConfigContainer, script_handler: ScriptHandler):
        """
        Initializes the ScriptContainer with configuration and script handler.

        Args:
            config (ConfigContainer): The configuration container providing script execution settings.
            script_handler (ScriptHandler): The handler responsible for executing scripts in the database.
        """
        self._config: ConfigContainer = config
        self._script_handler: ScriptHandler = script_handler

    def preflight_scripts(self, db: Session) -> None:
        """
        Executes the preflight script import process synchronously.

        These scripts are executed before other scripts to prepare the environment.
        Configurations are fetched from `preflight_scripts` in the config container.

        Args:
            db (Session): The synchronous database session.
        """
        return self._script_handler.execute_scripts(
            db=db,
            configs=self._config.preflight_scripts(),
        )

    def dependency_scripts(self, db: Session) -> None:
        """
        Executes the dependency script import process synchronously.

        These scripts handle dependency setup for the system. Configurations
        are fetched from `dependency_scripts` in the config container.

        Args:
            db (Session): The synchronous database session.
        """
        return self._script_handler.execute_scripts(
            db=db,
            configs=self._config.dependency_scripts(),
        )

    def attribute_scripts(self, db: Session) -> None:
        """
        Executes the attribute script import process synchronously.

        These scripts define and load attributes. Configurations
        are fetched from `attribute_scripts` in the config container.

        Args:
            db (Session): The synchronous database session.
        """
        return self._script_handler.execute_scripts(
            db=db,
            configs=self._config.attribute_scripts(),
        )

    def relationship_scripts(self, db: Session) -> None:
        """
        Executes the relationship script import process synchronously.

        These scripts establish relationships between different entities.
        Configurations are fetched from `relationship_scripts` in the config container.

        Args:
            db (Session): The synchronous database session.
        """
        return self._script_handler.execute_scripts(
            db=db,
            configs=self._config.relationship_scripts(),
        )

    def transformation_scripts(self, db: Session) -> None:
        """
        Executes the transformation script import process synchronously.

        These scripts apply transformations to the data.
        Configurations are fetched from `transformation_scripts` in the config container.

        Args:
            db (Session): The synchronous database session.
        """
        return self._script_handler.execute_scripts(
            db=db,
            configs=self._config.transformation_scripts(),
        )

    def gov_identifier_scripts(self, db: Session) -> None:
        """
        Executes the government identifier script import process synchronously.

        These scripts manage government-related identifiers.
        Configurations are fetched from `gov_identifier_scripts` in the config container.

        Args:
            db (Session): The synchronous database session.
        """
        return self._script_handler.execute_scripts(
            db=db,
            configs=self._config.gov_identifier_scripts(),
        )

    def call_report_scripts(self, db: Session) -> None:
        """
        Executes the call report script import process synchronously.

        These scripts handle call report data.
        Configurations are fetched from `call_report_scripts` in the config container.

        Args:
            db (Session): The synchronous database session.
        """
        return self._script_handler.execute_scripts(
            db=db,
            configs=self._config.call_report_scripts(),
        )
