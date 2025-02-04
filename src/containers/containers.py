from sqlalchemy import Engine

from .configs import ConfigContainer
from .imports import ImportContainer
from .scripts import ScriptContainer
from .workers import WorkersContainer
from ..registery.process import ProcessRegistery
from ..handlers import ConfigHandler, ImportHandler, ScriptHandler
from ..database.connection import intit_engine
from ..constants.database import CONNECTION_STRING


class DependencyContainer:
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
        engine: Engine,
        config_handler: ConfigHandler,
        import_handler: ImportHandler,
        script_handler: ScriptHandler,
    ):
        """
        Initializes the MasterContainer with necessary dependencies.

        Parameters:
            engine (Engine): The SQLAlchemy engine is used for database interactions.
            config_handler (ConfigHandler): The configuration handler is responsible for managing configurations.
            import_handler (ImportHandler): The import handler is responsible for managing data imports.
            script_handler (ScriptHandler): The script handler is responsible for managing configurations.
        """
        self._engine: Engine = engine
        self._config_handler: ConfigHandler = config_handler
        self._import_handler: ImportHandler = import_handler
        self._script_handler: ScriptHandler = script_handler

    def configs(self) -> ConfigContainer:
        """
        Creates and returns a ConfigContainer instance.

        Returns:
            ConfigContainer: An instance of ConfigContainer initialized with `_config_handler`.
        """
        return ConfigContainer(config_handler=self._config_handler)

    def imports(self) -> ImportContainer:
        """
        Creates and returns an ImportContainer instance.

        Returns:
            ImportContainer: An instance of ImportContainer initialized with a `ConfigContainer`,
                             `_engine`, and `_import_handler`.
        """
        return ImportContainer(
            config=self.configs(),
            engine=self._engine,
            import_handler=self._import_handler,
        )

    def scripts(self) -> ScriptContainer:
        """
        Creates and returns an ScriptContainer instance.

        Returns:
            ScriptContainer: An instance of ScriptContainer initialized with a `ConfigContainer`,
                             `_engine`, and `_script_handler`.
        """
        return ScriptContainer(
            config=self.configs(),
            engine=self._engine,
            script_handler=self._script_handler,
        )

    def workers(self) -> WorkersContainer:
        return WorkersContainer(imports=self.imports(), scripts=self.scripts())

    def registery(self) -> ProcessRegistery:
        return ProcessRegistery(workers=self.workers())


# Initialize database engine
engine = intit_engine(connection_string=CONNECTION_STRING, echo=False)


def dependency_container() -> DependencyContainer:
    """
    Creates and returns an instance of `DependencyContainer` with initialized dependencies.

    Returns:
        DepenencyContainer: An instance of DepenencyContainer initialized with `ConfigHandler`,
                         `ImportHandler`, and the database engine.
    """
    return DependencyContainer(
        engine=engine,
        config_handler=ConfigHandler,
        import_handler=ImportHandler,
        script_handler=ScriptHandler,
    )
