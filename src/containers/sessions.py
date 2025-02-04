from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from ..constants import connections


class SessionContainer:
    def __init__(self):
        pass

    def create_postgres_engine(self) -> Engine:
        return create_engine(url=connections.POSTGRES_CONNECTION, echo=False)
