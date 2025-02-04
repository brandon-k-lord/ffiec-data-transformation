from typing import List, Literal

import pandas as pd

from sqlalchemy import Engine
from ..logger import logger


class ImportHandler:

    @classmethod
    def _header_processor(cls, headers: List[str]) -> List[str]:
        """
        Normalizes headers read from files to simplify sql statements.

        Parameters:
        - headers: list of column headers
        """
        return [header.replace("#", "").lower().strip() for header in headers]

    @classmethod
    def to_sql_handler(
        cls,
        engine: Engine,
        file: str,
        table_schema: str,
        table_name: str,
        if_exists: Literal["append", "fail", "replace"],
        sep: Literal[",", "^"],
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
                    df.columns = cls._header_processor(headers=df.columns)
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

    @classmethod
    def import_handler(
        cls,
        engine: Engine,
        configs: List[dict],
    ) -> None:
        """
        Facilitates import based on configurations

        Parameters:
        - engine: connection
        - config: Import JSON
        """
        for config in configs:
            cls.to_sql_handler(
                engine=engine,
                file=config.get("file"),
                table_schema=config.get("table_name"),
                table_name=config.get("table_name"),
                if_exists=config.get("if_exists"),
                sep=config.get("sep", ","),
                cols=config.get("cols"),
                allow_import=config.get("allow_import", False),
            )
