from sqlalchemy import Engine
from .configs import ConfigContainer
from ..handlers import ImportHandler


# TODO: update documentation that engine must be passed directly
class ImportContainer:
    """
    A container class that manages various types of data imports by delegating tasks to an import handler.

    Attributes:
        _config (ConfigContainer): Holds configuration details for different types of imports.
        _import_handler (ImportHandler): Handles the execution of import operations.
        _engine (Engine): Database or processing engine used for executing imports.
    """

    def __init__(self, config: ConfigContainer, import_handler: ImportHandler):
        """
        Initializes the ImportContainer with configuration, import handler, and processing engine.

        Args:
            config (ConfigContainer): The configuration container providing import configurations.
            import_handler (ImportHandler): The handler responsible for executing imports.
            engine (Engine): The processing engine used for handling import operations.
        """
        self._config: ConfigContainer = config
        self._import_handler: ImportHandler = import_handler

    def bhcf_import(self, engine: Engine) -> None:
        """
        Executes the BHCF (Bank Holding Company Filings) import process.
        Uses the configurations provided by `bhcf_imports` from the config container.
        """
        return self._import_handler.import_handler(
            configs=self._config.bhcf_imports(),
            engine=engine,
        )

    def attribute_import(self, engine: Engine) -> None:
        """
        Executes the attributes import process.
        Uses the configurations provided by `attribute_imports` from the config container.
        """
        return self._import_handler.import_handler(
            configs=self._config.attribute_imports(),
            engine=engine,
        )

    def relationship_import(self, engine: Engine) -> None:
        """
        Executes the relationships import process.
        Uses the configurations provided by `relationship_imports` from the config container.
        """
        return self._import_handler.import_handler(
            configs=self._config.relationship_imports(),
            engine=engine,
        )

    def transformation_import(self, engine: Engine) -> None:
        """
        Executes the transformations import process.
        Uses the configurations provided by `transformation_imports` from the config container.
        """
        return self._import_handler.import_handler(
            configs=self._config.transformation_imports(),
            engine=engine,
        )

    def gov_identifier_import(self, engine: Engine) -> None:
        """
        Executes the gov_identifiers import process.
        Uses the configurations provided by `gov_identifier_imports` from the config container.
        """
        return self._import_handler.import_handler(
            configs=self._config.gov_identifier_imports(),
            engine=engine,
        )
