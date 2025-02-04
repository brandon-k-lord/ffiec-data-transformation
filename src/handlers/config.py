import os

from typing import List

from ..constants.dicts import FFEICConfig, ScriptsConfig


class ConfigHandler:
    @classmethod
    def _create_file_dict(directory: str) -> dict[str, str]:
        """
        Creates iterable dict of file paths.

        Key: filename
        value: absolute file path

        Parameters:
        - directory: directory name
        """
        wk_dir = os.path.join(os.getcwd(), directory)
        return {
            file.lower().split(".")[0]: os.path.join(wk_dir, file)
            for file in os.listdir(path=wk_dir)
        }

    @classmethod
    def _add_file_path(
        configs: List[FFEICConfig | ScriptsConfig], file_dict: dict[str, str]
    ):
        """Dynamically adds file paths to configs based on key_type and name."""

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
        return configs

    @classmethod
    def create_config(
        cls,
        directory: str,
        configs: List[FFEICConfig | ScriptsConfig],
    ) -> List[FFEICConfig | ScriptsConfig]:
        """
        Configures import JSON dynamically with {file: file_path}
        Immports and scripts are structured differently

        Parameters:
        - directory: directory path
        - config: Import JSON
        """
        file_dict: dict[str, str] = cls._create_file_dict(directory)
        return cls._add_file_path(configs=configs, file_dict=file_dict)
