import os
import pprint

import pandas as pd

from src.logger import logger
from src.data_handlers import load_import
from src.file_handlers import FileHandlers
from src.script_handlers import script_runner


class ImportConfig:
    def __init__(self) -> None:
        pass

    def import_configuration(self, directory: str, config: dict) -> dict:
        """
        Configures import JSON dynamically with {file: file_path}
        Immports and scripts are structured differently

        Parameters:
        - directory: directory path
        - config: Import JSON
        """

        import_dir = FileHandlers.file_directory(directory=directory)
        import_list = FileHandlers.file_list(directory=import_dir)

        for key, value in config.items():
            # comparing file name to key, dynamically add file path based on comparison conditions
            # mixture of statically named files and dynamically named that include date naming convention e.g., bhcf20240630
            if value["key_type"] == "prefix":
                for _key, _value in import_list.items():
                    if key == _key[:4]:
                        value["file"] = _value
            for _key, _value in import_list.items():
                if key == _key:
                    value["file"] = _value

        logger.info(
            f"service: import_configuration  |  config: {pprint.pformat(config)}"
        )

        return config

    def script_configuration(self, directory: str, config: dict) -> dict:
        """
        Configures import JSON dynamically with {file: file_path}
        Immports and scripts are structured differently

        Parameters:
        - directory: directory path
        - config: Script JSON
        """
        script_directory = FileHandlers.file_directory(directory=directory)
        files = os.listdir(path=script_directory)
        logger.info(script_directory)
        logger.info(files)

        file_dict = {}
        for file in files:
            file_dict[file] = os.path.join(script_directory, file)

        for value in config["scripts"]:

            i = value["filename"]
            for _key, _value in file_dict.items():
                if _key == i:
                    value["file"] = _value

    def intit_scripts(self, engine: object, config: dict):
        """
        Facilitates script execution based on configurations

        Parameters:
        - engine: connection
        - config: Script JSON
        """
        for value in config["scripts"]:
            script = value["file"]
            allow_exe = value["allow_exe"]
            if allow_exe:
                logger.info(
                    f"service: init_scripts  |  allow_exe:  {allow_exe}  |  executing file: {script}"
                )
                script_runner(engine=engine, script=script)

    def init_import(self, engine: object, config: dict):
        """
        Facilitates import based on configurations

        Parameters:
        - engine: connection
        - config: Import JSON
        """
        for key, value in config.items():
            file = value["file"]
            logger.info(file)
            table_schema = value["table_schema"]
            table_name = value["table_name"]
            if_exists = value["if_exists"]
            sep = value["sep"]
            cols = value["cols"]
            allow_import = value["allow_import"]

            file_loaded = load_import(
                engine=engine,
                file=file,
                table_schema=table_schema,
                table_name=table_name,
                if_exists=if_exists,
                sep=sep,
                cols=cols,
                allow_import=allow_import,
            )

            if file_loaded:
                logger.info(
                    f"service: init_import  |  allow_import:  {allow_import}  |  Loaded: file: {file}  |  table_schema:  {table_schema} | table_name:  {table_name}"
                )
