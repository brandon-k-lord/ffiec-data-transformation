from typing import List
from ..constants import scripts
from ..constants import imports
from ..constants import directories
from ..constants.dicts import FFEICConfig, ScriptsConfig

from ..handlers import ConfigHandler

from typing import List


class ConfigContainer:
    """
    A container class that provides configuration imports for different datasets and scripts.

    This class acts as a wrapper around a `ConfigHandler` instance, enabling retrieval
    of predefined configurations for various imports and script executions.

    Attributes:
        _config_handler (ConfigHandler): An instance of ConfigHandler responsible for
                                         generating configuration dictionaries.
    """

    _import_file_dict: dict[str, str] | None = None
    _script_file_dict: dict[str, str] | None = None

    def __init__(self, config_handler: ConfigHandler):
        """
        Initializes the ConfigContainer with a ConfigHandler instance.

        Parameters:
            config_handler (ConfigHandler): The configuration handler responsible for
                                            creating configurations dynamically.
        """
        self._config_handler: ConfigHandler = config_handler

    def get_import_file_dict(
        self, directory: str = directories.IMPORT
    ) -> dict[str, str]:
        if self._import_file_dict is None:
            self._import_file_dict = self._config_handler.create_file_dict(
                directory=directory
            )

        return self._import_file_dict

    def get_script_file_dict(
        self, directory: str = directories.SCRIPTS
    ) -> dict[str, str]:
        if self._import_script_dict is None:
            self._import_script_dict = self._config_handler.create_file_dict(
                directory=directory
            )

        return self._import_script_dict

    def bhcf_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for FFIEC BHCF imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.BHCF, file_dict=self.get_import_file_dict()
        )

    def attribute_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for FFIEC Attribute imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.ATTRIBUTES, file_dict=self.get_import_file_dict()
        )

    def relationship_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for FFIEC Relationship imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.RELATIONSHIPS, file_dict=self.get_import_file_dict()
        )

    def transformation_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for FFIEC Transformation imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.TRANSFORMATIONS, file_dict=self.get_import_file_dict()
        )

    def gov_identifier_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for government identifiers imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.GOV_IDENTIFIERS, file_dict=self.get_import_file_dict()
        )

    def preflight_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for preflight scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.PREFLIGHT,
            file_dict=self.get_script_file_dict(),
        )

    def dependency_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for dependency scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.DEPENDENCIES,
            file_dict=self.get_script_file_dict(),
        )

    def attribute_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for attribute scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.ATTRIBUTES,
            file_dict=self.get_script_file_dict(),
        )

    def relationship_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for relationship scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.RELATIONSHIPS,
            file_dict=self.get_script_file_dict(),
        )

    def transformation_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for transformation scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.TRANSFORMATIONS,
            file_dict=self.get_script_file_dict(),
        )

    def gov_identifier_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for government identifiers scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.GOV_IDENTIFIERS,
            file_dict=self.get_script_file_dict(),
        )

    def call_report_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for call report scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.CALL_REPORTS,
            file_dict=self.get_script_file_dict(),
        )
