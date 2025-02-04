from sqlalchemy import Engine

from .configs import ConfigContainer
from .imports import ImportContainer
from .scripts import ScriptContainer
from .workers import WorkersContainer
from ..registry.process import ProcessRegistry
from ..handlers import ConfigHandler, ImportHandler, ScriptHandler
from ..database.connection import init_engine
from ..constants.database import CONNECTION_STRING


class DependencyContainer:
    """
    A container class that manages and provides access to application dependencies.

    This class centralizes and initializes dependencies required for configuration handling,
    data imports, script execution, and worker management. It ensures that different components
    can interact seamlessly by maintaining shared instances.

    Attributes:
        _engine (Engine): A SQLAlchemy database engine for database interactions.
        _config_handler (ConfigHandler): Handles configuration settings.
        _import_handler (ImportHandler): Manages data import operations.
        _script_handler (ScriptHandler): Manages script execution.
    """

    def __init__(
        self,
        engine: Engine,
        config_handler: ConfigHandler,
        import_handler: ImportHandler,
        script_handler: ScriptHandler,
    ):
        """
        Initializes the DependencyContainer with required service handlers and the database engine.

        Parameters:
            engine (Engine): SQLAlchemy engine used for database interactions.
            config_handler (ConfigHandler): Handles application configurations.
            import_handler (ImportHandler): Manages data import operations.
            script_handler (ScriptHandler): Manages script execution.
        """
        self._engine: Engine = engine
        self._config_handler: ConfigHandler = config_handler
        self._import_handler: ImportHandler = import_handler
        self._script_handler: ScriptHandler = script_handler

    def configs(self) -> ConfigContainer:
        """
        Creates and returns a ConfigContainer instance for managing application configurations.

        Returns:
            ConfigContainer: An instance initialized with `_config_handler`.
        """
        return ConfigContainer(config_handler=self._config_handler)

    def imports(self) -> ImportContainer:
        """
        Creates and returns an ImportContainer instance for managing data imports.

        Returns:
            ImportContainer: An instance initialized with `ConfigContainer`, `_engine`,
                             and `_import_handler` to facilitate data import processes.
        """
        return ImportContainer(
            config=self.configs(),
            engine=self._engine,
            import_handler=self._import_handler,
        )

    def scripts(self) -> ScriptContainer:
        """
        Creates and returns a ScriptContainer instance for executing scripts.

        Returns:
            ScriptContainer: An instance initialized with `ConfigContainer`, `_engine`,
                             and `_script_handler` to facilitate script execution.
        """
        return ScriptContainer(
            config=self.configs(),
            engine=self._engine,
            script_handler=self._script_handler,
        )

    def workers(self) -> WorkersContainer:
        """
        Creates and returns a WorkersContainer instance for handling parallel execution of imports and scripts.

        Returns:
            WorkersContainer: An instance initialized with `ImportContainer` and `ScriptContainer`,
                              allowing concurrent execution of import and script tasks.
        """
        return WorkersContainer(imports=self.imports(), scripts=self.scripts())

    def registry(self) -> ProcessRegistry:
        """
        Creates and returns a ProcessRegistry instance to manage process execution.

        Returns:
            ProcessRegistry: An instance initialized with `WorkersContainer`,
                              providing centralized process management.
        """
        return ProcessRegistry(workers=self.workers())


# Initialize database engine
engine = init_engine(connection_string=CONNECTION_STRING, echo=False)


def get_dependency_container() -> DependencyContainer:
    """
    Creates and returns an instance of `DependencyContainer` with initialized dependencies.

    Returns:
        DependencyContainer: An instance initialized with `ConfigHandler`, `ImportHandler`,
                             `ScriptHandler`, and the database engine.
    """
    return DependencyContainer(
        engine=engine,
        config_handler=ConfigHandler,
        import_handler=ImportHandler,
        script_handler=ScriptHandler,
    )
