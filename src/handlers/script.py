"""
script

This module provides functionality for executing SQL scripts in a synchronous database session. 
It defines the `ScriptHandler` class, which allows running individual SQL scripts as well as 
batch execution of multiple scripts based on configurable parameters.
"""

import logging
from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..constants.objects import ScriptsConfig
from ..logger import logger

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class ScriptHandler:
    """
    A handler for executing SQL scripts against a database.

    This class provides methods to run individual SQL scripts and execute multiple
    scripts based on configuration settings.
    """

    @classmethod
    def _script_runner(cls, db: Session, script: str) -> None:
        """
        Executes an SQL script using the provided database session.

        Args:
            db (Session): SQLAlchemy database session for executing queries.
            script (str): Path to the SQL script file to be executed.

        Raises:
            Exception: Logs an error if the script execution fails.
        """
        try:
            with open(script, "r") as file:
                sql_script = file.read()

            with db.begin():
                db.execute(text(sql_script))
        except Exception as e:
            logger.error(f"Failed to execute {script}: {str(e)}")

    @classmethod
    def execute_scripts(cls, db: Session, configs: List[ScriptsConfig]) -> None:
        """
        Executes multiple SQL scripts based on the provided configurations.

        Args:
            db (Session): SQLAlchemy database session for executing queries.
            configs (List[ScriptsConfig]): List of script configurations, each containing:
                - file_path (str): Path to the SQL script file.
                - allow_exe (bool): Flag indicating whether the script should be executed.

        Logs:
            - Info logs for scripts that are executed or skipped.
            - Error logs if script execution fails.
        """
        for config in configs:
            if config.get("allow_exe"):
                logger.info(
                    f"service: init_scripts | executing file: {config.get('file_path')}"
                )
                cls._script_runner(db=db, script=config.get("file_path"))
            else:
                logger.info(
                    f"Skipping execution for {config.get('file_path')} due to 'allow_exe' being False"
                )
