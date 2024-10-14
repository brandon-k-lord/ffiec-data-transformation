from sqlalchemy import create_engine, text

from config import settings


def intit_engine():
    connection_string = f"{settings.db_driver}://{settings.db_usrnm}:{settings.db_pwd}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    return create_engine(connection_string, echo=False)


def init_table_schema(schema: str, engine: object):
    with engine.connect() as conn:
        stm = f"create schema if not exists {schema};"
        conn.execute(text(stm))
        conn.commit()
    return
