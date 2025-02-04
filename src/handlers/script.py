import logging

from typing import List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..constants.dicts import ScriptsConfig
from ..logger import logger

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


class ScriptHandler:

    @classmethod
    async def _script_runner(cls, db: AsyncSession, script: str) -> None:
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

            async with db.begin():
                await db.execute(text(sql_script))
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to execute {script}: {str(e)}")

    @classmethod
    async def execute_scripts(
        cls, db: AsyncSession, configs: List[ScriptsConfig]
    ) -> None:
        """
        Executes multiple SQL scripts based on the provided configurations.

        Args:
            engine (Engine): SQLAlchemy database engine for executing queries.
            configs (List[ScriptsConfig]): List of script configurations, each containing:
                - file_path (str): Path to the SQL script file.
                - allow_exe (bool): Flag to determine if the script should be executed.
        """
        for config in configs:
            script = config.get("file_path")
            allow_exe = config.get("allow_exe", False)
            if allow_exe:
                logger.info(f"service: init_scripts | executing file: {script}")
                await cls._script_runner(db=db, script=script)
            else:
                logger.info(
                    f"Skipping execution for {script} due to 'allow_exe' being False"
                )
