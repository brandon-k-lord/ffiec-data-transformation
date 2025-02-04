from sqlalchemy import Engine, create_engine, text

def intit_engine(connection_string:str, echo:bool)->Engine:
    return create_engine(url=connection_string, echo=False)


def init_table_schema(schema: str, engine: Engine)->None:
    """
    Ensures table schema exists

    Parameters:
    - schema: name of schema for validation/creation
    - engine: connection
    """
    with engine.connect() as conn:
        stm = f"create schema if not exists {schema};"
        conn.execute(text(stm))
        conn.commit()
