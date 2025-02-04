import logging

from typing import List
from sqlalchemy import Engine, text

from ..constants.dicts import ScriptsConfig
from ..logger import logger

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class ScriptHandler:

    @classmethod
    def _script_runner(cls, engine: Engine, script: str) -> None:
        """
        Executes an SQL script using the provided database engine.

        Args:
            engine (Engine): SQLAlchemy database engine for executing queries.
            script (str): Path to the SQL script file to be executed.

        Raises:
            Exception: Logs an error if the script execution fails.
        """
        try:
            with open(script, "r") as file:
                sql_script = file.read()

            with engine.begin() as conn:
                conn.execute(text(sql_script))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to execute {script}: {str(e)}")

    @classmethod
    def execute_scripts(cls, engine: Engine, configs: List[ScriptsConfig]) -> None:
        """
        Executes multiple SQL scripts based on the provided configurations.

        Args:
            engine (Engine): SQLAlchemy database engine for executing queries.
            configs (List[ScriptsConfig]): List of script configurations, each containing:
                - file (str): Path to the SQL script file.
                - allow_exe (bool): Flag to determine if the script should be executed.
        """
        for config in configs:
            script = config["file"]
            allow_exe = config["allow_exe"]
            if allow_exe:
                logger.info(f"service: init_scripts | executing file: {script}")
                cls._script_runner(engine=engine, script=script)
            else:
                logger.info(
                    f"Skipping execution for {script} due to 'allow_exe' being False"
                )
