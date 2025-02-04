from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session
from ..database.db import DBInitializer
from ..constants import connections
from ..constants import schemas


class DatabaseContainer:

    def __init__(self, db: DBInitializer):
        self._db_initializer: DBInitializer = db_initializer

    def _create_postgres_engine(self) -> Engine:
        return self._db_initializer.get_engine(
            connection_string=connections.POSTGRES_CONNECTION
        )

    def _postgres_session(self):
        return sessionmaker(
            bind=self._create_postgres_engine(),
            autoflush=False,
            class_=Session,
            expire_on_commit=False,
        )

    def get_postgres_db(self):

        with self._postgres_session() as db:
            try:
                yield db
            finally:
                db.close()

    def create_transformation_schema(self):
        return DBInitializer.create_table_schema(
            engine=self.get_postgres_db(), schema=schemas
        )
