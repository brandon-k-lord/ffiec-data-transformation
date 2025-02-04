import os

import pprint
from typing import List

from ..constants.dicts import FFEICConfig, ScriptsConfig
from ..logger import logger


class ConfigHandler:
    @classmethod
    def create_file_dict(cls, directory: str) -> dict[str, str]:
        """
        Creates iterable dict of file paths.

        Key: filename
        value: absolute file path

        Parameters:
        - directory: directory name
        """
        wk_dir = os.path.join(os.getcwd(), directory)

        # TODO: We can do this jsut once instead of each time.

        return {
            file.lower().split(".")[0]: os.path.join(wk_dir, file)
            for file in os.listdir(path=wk_dir)
        }

    @classmethod
    def _add_file_path(
        cls, configs: List[FFEICConfig | ScriptsConfig], file_dict: dict[str, str]
    ):
        """Dynamically adds file paths to configs based on key_type and name."""
        # TODO: Remove logger
        logger.info("File Dictionary: %s", pprint.pformat(file_dict, indent=2))
        for config in configs:

            config["file_path"] = next(
                (
                    value
                    for key, value in file_dict.items()
                    if (
                        "key_type" in config
                        and config["key_type"] == "prefix"
                        and config["name"] == key[:4]
                    )
                    or (config["name"] == key)
                ),
                None,
            )

        # TODO: Remove logger
        logger.info("Configs: %s", pprint.pformat(configs, indent=2))
        return configs

    @classmethod
    def create_config(
        cls,
        configs: List[FFEICConfig | ScriptsConfig],
        file_dict: dict[str, str],
    ) -> List[FFEICConfig | ScriptsConfig]:
        """
        Configures import JSON dynamically with {file: file_path}
        Immports and scripts are structured differently

        Parameters:
        - directory: directory path
        - config: Import JSON
        """
        return cls._add_file_path(configs=configs, file_dict=file_dict)
