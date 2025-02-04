from typing import Callable, List, Literal, Optional

import pandas as pd

from sqlalchemy import Engine


from ..constants.dicts import FFEICConfig, ScriptsConfig
from ..logger import logger


class ImportHandler:
    @staticmethod
    def create_config(
        directory: str,
        configs: List[FFEICConfig | ScriptsConfig],
        create_file_dict: Callable[[str], dict[str, str]],
    ) -> List[FFEICConfig | ScriptsConfig]:
        """
        Configures import JSON dynamically with {file: file_path}
        Immports and scripts are structured differently

        Parameters:
        - directory: directory path
        - config: Import JSON
        """
        file_dict: dict[str, str] = create_file_dict(directory)

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

        return _add_file_path(configs=configs, file_dict=file_dict)

    @staticmethod
    def import_loader(
        engine: Engine,
        file: str,
        table_schema: str,
        table_name: str,
        if_exists: Literal["append", "fail", "replace"],
        sep: Literal[",", "^"],
        normalize_headers: Callable[[List[str]], List[str]],
        cols: List[str] = None,
        allow_import: bool = False,
    ) -> None:
        """

        Parameters:
        - engine: Connection
        - file: File path
        - table_schema: Name of target table schema
        - table_name: Name of target table
        - if_exists: Action for if table exists
        - sep: Seperator for reading files e.g., ",", "^"
        - cols: Specifices a list of columns for filtering import data, imports all data if empty
        - allow_import: Boolean flag signaling if file is allowed to be imoprted
        """
        if not allow_import:
            return
        try:
            with engine.begin() as conn:
                logger.info(
                    f"service: load_import  |  allow_import:  {allow_import}  |  Reading: file: {file}  |  table_schema:  {table_schema} | table_name:  {table_name}"
                )
                df = pd.read_csv(
                    filepath_or_buffer=file, engine="python", sep=sep, encoding="utf-8"
                )

                if cols is None:
                    df.columns = normalize_headers(headers=df.columns)
                else:
                    df = df[cols]

                logger.info(
                    f"service: load_import  |  allow_import:  {allow_import}  |  Loading: file: {file}  |  table_schema:  {table_schema} | table_name:  {table_name}"
                )
                logger.info(
                    f"service: load_import  |  message: Loading dataframe to the database, this may take serveral seconds for larger files..."
                )
                df.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists=if_exists,
                    schema=table_schema,
                    index=False,
                )
        except Exception as e:
            logger.warning(f"UnhandledError: {e}")

    @staticmethod
    def import_handler(
        engine: Engine,
        configs: List[dict],
        import_loader: Callable[
            [
                Engine,
                str,
                str,
                str,
                Literal["append", "fail", "replace"],
                Literal[",", "^"],
                Callable[[List[str]], List[str]],
                Optional[List[str]],
                bool,
            ],
            None,
        ],
    ) -> None:
        """
        Facilitates import based on configurations

        Parameters:
        - engine: connection
        - config: Import JSON
        """
        for config in configs:
            file = config["file"]
            logger.info(file)
            table_schema = config["table_schema"]
            table_name = config["table_name"]
            if_exists = config["if_exists"]
            sep = config["sep"]
            cols = config["cols"]
            allow_import = config["allow_import"]

            import_loader(
                engine=engine,
                file=file,
                table_schema=table_schema,
                table_name=table_name,
                if_exists=if_exists,
                sep=sep,
                cols=cols,
                allow_import=allow_import,
            )
