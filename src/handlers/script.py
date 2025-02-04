import logging

from typing import List
from sqlalchemy import Engine, text

from ..constants.dicts import ScriptsConfig
from ..logger import logger

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def script_runner(engine: Engine, script: str):
    """
    Parameters:
    - engine: Connection
    - script: Executable SQL file
    """
    try:
        with open(script, "r") as file:
            sql_script = file.read()

        with engine.begin() as conn:
            conn.execute(text(sql_script))
            conn.commit()
    except Exception as e:
        logger.error(f"Failed to execute {script}: {str(e)}")


def execute_scripts(engine: Engine, configs: List[ScriptsConfig]) -> None:
    """
    Facilitates script execution based on configurations

    Parameters:
    - engine: connection
    - config: Script JSON
    """
    for config in configs:
        script = config["file"]
        allow_exe = config["allow_exe"]
        if allow_exe:
            logger.info(f"service: init_scripts | executing file: {script}")
            script_runner(engine=engine, script=script)
        else:
            logger.info(
                f"Skipping execution for {script} due to 'allow_exe' being False"
            )
