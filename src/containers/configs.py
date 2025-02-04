from typing import List
from ..constants import directories
from ..constants import scripts
from ..constants import imports
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

    def __init__(self, config_handler: ConfigHandler):
        """
        Initializes the ConfigContainer with a ConfigHandler instance.

        Parameters:
            config_handler (ConfigHandler): The configuration handler responsible for
                                            creating configurations dynamically.
        """
        self._config_handler: ConfigHandler = config_handler

    def bhcf_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for FFIEC BHCF imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.BHCF,
            directory=directories.IMPORT,
        )

    def attribute_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for FFIEC Attribute imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.ATTRIBUTES,
            directory=directories.IMPORT,
        )

    def relationship_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for FFIEC Relationship imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.RELATIONSHIPS,
            directory=directories.IMPORT,
        )

    def transformation_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for FFIEC Transformation imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.TRANSFORMATIONS,
            directory=directories.IMPORT,
        )

    def gov_identifier_imports(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for government identifiers imports.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to BHCF imports.
        """
        return self._config_handler.create_config(
            configs=imports.GOV_IDENTIFIERS,
            directory=directories.IMPORT,
        )

    def preflight_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for preflight scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.PREFLIGHT,
            directory=directories.SCRIPTS,
        )

    def dependency_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for dependency scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.DEPENDENCIES,
            directory=directories.SCRIPTS,
        )

    def attribute_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for attribute scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.ATTRIBUTES,
            directory=directories.SCRIPTS,
        )

    def relationship_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for relationship scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.RELATIONSHIPS,
            directory=directories.SCRIPTS,
        )

    def transformation_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for transformation scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.TRANSFORMATIONS,
            directory=directories.SCRIPTS,
        )

    def gov_identifier_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for government identifiers scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.GOV_IDENTIFIERS,
            directory=directories.SCRIPTS,
        )

    def call_report_scripts(self) -> List[FFEICConfig | ScriptsConfig]:
        """
        Retrieves the configuration for call report scripts.

        Returns:
            List[FFEICConfig | ScriptsConfig]: A list of configurations specific to preflight scripts.
        """
        return self._config_handler.create_config(
            configs=scripts.CALL_REPORTS,
            directory=directories.SCRIPTS,
        )
