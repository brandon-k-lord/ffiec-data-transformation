"""
imports

This module contains the `ImportContainer` class, which manages different types of data import processes
by delegating tasks to an import handler. It provides functionality to execute various import processes
such as BHCF, attributes, relationships, transformations, and government identifiers, using configurations
provided by the `ConfigContainer` and processing handled by the `ImportHandler`.

Classes:
    ImportContainer: A container class that manages and executes different types of data imports using
                     the provided `ImportHandler` and configurations from the `ConfigContainer`.
Notes:
    The engine used for executing imports must be passed directly to the `ImportContainer` methods.
"""

from sqlalchemy import Engine

from ..handlers import ImportHandler
from .config import ConfigContainer


class ImportContainer:
    """
    A container class that manages and executes various types of data imports by delegating tasks to an import handler.

    This class facilitates the execution of different import processes, such as BHCF, attributes, relationships,
    transformations, and government identifiers. It retrieves import configurations from the `ConfigContainer` and
    processes them using the `ImportHandler`. The `engine` used for executing imports must be passed to each method
    explicitly.

    Attributes:
        _config (ConfigContainer): Provides configuration details for different types of imports.
        _import_handler (ImportHandler): Responsible for handling the execution of import operations.
    """

    def __init__(self, config: ConfigContainer, import_handler: ImportHandler):
        """
        Initializes the ImportContainer with a configuration container and an import handler.

        Args:
            config (ConfigContainer): The configuration container providing import settings.
            import_handler (ImportHandler): The handler responsible for executing import operations.
        """
        self._config: ConfigContainer = config
        self._import_handler: ImportHandler = import_handler

    def bhcf_import(self, engine: Engine) -> None:
        """
        Executes the BHCF (Bank Holding Company Filings) import process.

        This method retrieves configurations from the `bhcf_imports` method of the `ConfigContainer`
        and processes them using the `ImportHandler`.

        Args:
            engine (Engine): The database or processing engine used for execution.
        """
        return self._import_handler.import_handler(
            configs=self._config.bhcf_imports(),
            engine=engine,
        )

    def attribute_import(self, engine: Engine) -> None:
        """
        Executes the attribute import process.

        This method retrieves configurations from the `attribute_imports` method of the `ConfigContainer`
        and processes them using the `ImportHandler`.

        Args:
            engine (Engine): The database or processing engine used for execution.
        """
        return self._import_handler.import_handler(
            configs=self._config.attribute_imports(),
            engine=engine,
        )

    def relationship_import(self, engine: Engine) -> None:
        """
        Executes the relationship import process.

        This method retrieves configurations from the `relationship_imports` method of the `ConfigContainer`
        and processes them using the `ImportHandler`.

        Args:
            engine (Engine): The database or processing engine used for execution.
        """
        return self._import_handler.import_handler(
            configs=self._config.relationship_imports(),
            engine=engine,
        )

    def transformation_import(self, engine: Engine) -> None:
        """
        Executes the transformation import process.

        This method retrieves configurations from the `transformation_imports` method of the `ConfigContainer`
        and processes them using the `ImportHandler`.

        Args:
            engine (Engine): The database or processing engine used for execution.
        """
        return self._import_handler.import_handler(
            configs=self._config.transformation_imports(),
            engine=engine,
        )

    def gov_identifier_import(self, engine: Engine) -> None:
        """
        Executes the government identifier import process.

        This method retrieves configurations from the `gov_identifier_imports` method of the `ConfigContainer`
        and processes them using the `ImportHandler`.

        Args:
            engine (Engine): The database or processing engine used for execution.
        """
        return self._import_handler.import_handler(
            configs=self._config.gov_identifier_imports(),
            engine=engine,
        )
