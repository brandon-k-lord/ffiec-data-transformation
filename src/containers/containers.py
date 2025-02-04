from sqlalchemy import Engine

from .configs import ConfigContainer
from .imports import ImportContainer
from ..handlers import ConfigHandler, ImportHandler
from ..database.connection import intit_engine
from ..constants.database import CONNECTION_STRING


class MasterContainer:
    """
    A container class that provides access to configuration and import handling.

    This class initializes and manages dependencies for `ConfigContainer` and `ImportContainer`,
    ensuring that configuration settings and import operations are easily accessible.

    Attributes:
        _config_handler (ConfigHandler): An instance of ConfigHandler for managing configurations.
        _import_handler (ImportHandler): An instance of ImportHandler for handling data imports.
        _engine (Engine): A SQLAlchemy database engine used for database interactions.
    """

    def __init__(
        self,
        config_handler: ConfigHandler,
        import_handler: ImportHandler,
        engine: Engine,
    ):
        """
        Initializes the MasterContainer with necessary dependencies.

        Parameters:
            config_handler (ConfigHandler): The configuration handler responsible for managing configurations.
            import_handler (ImportHandler): The import handler responsible for managing data imports.
            engine (Engine): The SQLAlchemy engine used for database interactions.
        """
        self._config_handler: ConfigHandler = config_handler
        self._import_handler: ImportHandler = import_handler
        self._engine: Engine = engine

    def config_container(self) -> ConfigContainer:
        """
        Creates and returns a ConfigContainer instance.

        Returns:
            ConfigContainer: An instance of ConfigContainer initialized with `_config_handler`.
        """
        return ConfigContainer(config_handler=self._config_handler)

    def import_container(self) -> ImportContainer:
        """
        Creates and returns an ImportContainer instance.

        Returns:
            ImportContainer: An instance of ImportContainer initialized with a `ConfigContainer`,
                             `_engine`, and `_import_handler`.
        """
        return ImportContainer(
            config=self.config_container(),
            engine=self._engine,
            import_handler=self._import_handler,
        )


# Initialize database engine
engine = intit_engine(connection_string=CONNECTION_STRING, echo=False)


def master_container() -> MasterContainer:
    """
    Creates and returns an instance of `MasterContainer` with initialized dependencies.

    Returns:
        MasterContainer: An instance of MasterContainer initialized with `ConfigHandler`,
                         `ImportHandler`, and the database engine.
    """
    return MasterContainer(
        engine=engine, config_handler=ConfigHandler, import_handler=ImportHandler
    )
