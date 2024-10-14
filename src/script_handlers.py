import logging

from sqlalchemy import text

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def script_runner(engine: object, script: str):

    with open(script, "r") as file:
        sql_script = file.read()

    with engine.begin() as conn:
        conn.execute(text(sql_script))
        conn.commit()
