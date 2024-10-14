from typing import Annotated, Literal, List
import pandas as pd

from src.logger import logger


def normalize_col_headers(headers: list) -> list:
    """
    Normalizes headers read from files to simplify sql statements

    Parameters:
    - headers: list of column headers
    """
    std_headers = [header.replace("#", "").lower().strip() for header in headers]

    return std_headers


def load_import(
    engine: object,
    file: str,
    table_schema: str,
    table_name: str,
    if_exists: Literal["append", "fail", "replace"],
    sep: Literal[",", "^"],
    cols: List = None,
    allow_import: bool = False,
):
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
        f"service: load_import  |  allow_import:  {allow_import}  |  Loading: file: {file}  |  table_schema:  {table_schema} | table_name:  {table_name}"
        return
    try:
        with engine.begin() as conn:
            logger.info(
                f"service: load_import  |  allow_import:  {allow_import}  |  Reading: file: {file}  |  table_schema:  {table_schema} | table_name:  {table_name}"
            )
            df = pd.read_csv(
                filepath_or_buffer=file, engine="python", sep=sep, encoding="utf-8"
            )

            # it is easier to filter some files here prior to importing
            if not cols:
                df.columns = normalize_col_headers(headers=df.columns)
            else:
                df = df[cols]

            logger.info(
                f"service: load_import  |  allow_import:  {allow_import}  |  Loading: file: {file}  |  table_schema:  {table_schema} | table_name:  {table_name}"
            )
            logger.info(
                f"service: load_import  |  message: Loading dataframe to the database, this may take serveral seconds for larger files..."
            )

            # writes file to database
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists=if_exists,
                schema=table_schema,
                index=False,
            )
            return True
    except Exception as e:
        logger.warning(f"UnhandledError: {e}")
        return False
