"""
dependency

This module contains the `DependencyContainer` class, which centralizes and provides access to
various application dependencies. These dependencies include handlers and containers for configuration,
data imports, script execution, worker management, schema handling, and session management.
It ensures that these components can be accessed modularly throughout the application.

Classes:
    DependencyContainer: A container class that manages and provides access to shared application
                         components and services such as configuration handling, data imports,
                         script execution, worker management, schema handling, and session management.
"""

from ..handlers import ConfigHandler, ImportHandler, SchemaHandler, ScriptHandler
from .config import ConfigContainer
from .imports import ImportContainer
from .registry import RegistryContainer
from .schema import SchemaContainer
from .script import ScriptContainer
from .session import SessionContainer
from .worker import WorkerContainer


class DependencyContainer:
    """
    A container class that centralizes and provides access to application dependencies.

    This class initializes and manages shared instances of key components required for
    configuration handling, data imports, script execution, worker management, schema handling,
    and session management. It ensures modular access to these dependencies across the application.

    Attributes:
        _config_handler (ConfigHandler): Handles application configuration settings.
        _import_handler (ImportHandler): Manages data import operations.
        _schema_handler (SchemaHandler): Handles schema-related operations.
        _script_handler (ScriptHandler): Manages script execution.
    """

    def __init__(
        self,
        config_handler: ConfigHandler,
        import_handler: ImportHandler,
        schema_handler: SchemaHandler,
        script_handler: ScriptHandler,
    ):
        """
        Initializes the DependencyContainer with required service handlers.

        Parameters:
            config_handler (ConfigHandler): Handles application configurations.
            import_handler (ImportHandler): Manages data import operations.
            schema_handler (SchemaHandler): Handles schema-related operations.
            script_handler (ScriptHandler): Manages script execution.
        """
        self._config_handler: ConfigHandler = config_handler
        self._import_handler: ImportHandler = import_handler
        self._schema_handler: SchemaHandler = schema_handler
        self._script_handler: ScriptHandler = script_handler

    def config(self) -> ConfigContainer:
        """
        Creates and returns a ConfigContainer instance for managing application configurations.

        Returns:
            ConfigContainer: An instance initialized with `_config_handler`.
        """
        return ConfigContainer(config_handler=self._config_handler)

    def import_(self) -> ImportContainer:
        """
        Creates and returns an ImportContainer instance for managing data imports.

        Returns:
            ImportContainer: An instance initialized with `ConfigContainer` and `_import_handler`
                             to facilitate data import processes.
        """
        return ImportContainer(
            config=self.config(),
            import_handler=self._import_handler,
        )

    def worker(self) -> WorkerContainer:
        """
        Creates and returns a WorkerContainer instance for handling parallel execution of imports and scripts.

        Returns:
            WorkerContainer: An instance initialized with `ImportContainer` and `ScriptContainer`,
                              allowing concurrent execution of import and script tasks.
        """
        return WorkerContainer(
            import_=self.import_(), script=self.script(), session=self.session()
        )

    def registry(self) -> RegistryContainer:
        """
        Creates and returns a RegistryContainer instance to manage process execution.

        Returns:
            RegistryContainer: An instance initialized with `WorkerContainer` and `SessionContainer`,
                               providing centralized process management.
        """
        return RegistryContainer(
            worker=self.worker(), session=self.session(), schema=self.schema()
        )

    def script(self) -> ScriptContainer:
        """
        Creates and returns a ScriptContainer instance for executing scripts.

        Returns:
            ScriptContainer: An instance initialized with `ConfigContainer` and `_script_handler`
                             to facilitate script execution.
        """
        return ScriptContainer(
            config=self.config(),
            script_handler=self._script_handler,
        )

    def session(self) -> SessionContainer:
        """
        Creates and returns a SessionContainer instance for session management.

        Returns:
            SessionContainer: A new instance to handle session-related functionality.
        """
        return SessionContainer()

    def schema(self) -> SchemaContainer:
        """
        Creates and returns a SchemaContainer instance for schema management.

        Returns:
            SchemaContainer: An instance initialized with `_schema_handler` to manage schema operations.
        """
        return SchemaContainer(schema_handler=self._schema_handler)


def get_dependency_container() -> DependencyContainer:
    """
    Creates and returns an instance of `DependencyContainer` with initialized dependencies.

    Returns:
        DependencyContainer: An instance initialized with `ConfigHandler`, `ImportHandler`,
                             `SchemaHandler`, and `ScriptHandler`.
    """
    return DependencyContainer(
        config_handler=ConfigHandler(),
        import_handler=ImportHandler(),
        schema_handler=SchemaHandler(),
        script_handler=ScriptHandler(),
    )
