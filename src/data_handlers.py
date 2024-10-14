from typing import Annotated, Literal, List
import pandas as pd

from src.logger import logger


def normalize_col_headers(headers: list) -> list:
    """cleans headers of space and limited special character support"""
    std_headers = [header.replace("#", "").lower().strip() for header in headers]

    return std_headers


def load_import(
    engine: object,
    file: str,
    table_schema: str,
    table_name: str,
    if_exists: Literal["append", "fail", "replace"],
    sep: Literal[",", "^"],
    # load_type: Literal["full", "partial"],
    cols: List = None,
    allow_import: bool = False,
):
    """function will read csv file and write to database based on specified locations"""
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
            if not cols:
                df.columns = normalize_col_headers(headers=df.columns)
            else:
                df = df[cols]

            print(df)
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
            return True
    except Exception as e:
        logger.warning(f"UnhandledError: {e}")
        return False
