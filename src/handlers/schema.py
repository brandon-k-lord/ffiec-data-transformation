"""
schema_handler

This module provides functionality for managing database schemas. It defines 
the `SchemaHandler` class, which ensures the existence of schemas in the 
database and creates them if they do not exist.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session  # Changed for sync execution


class SchemaHandler:
    """
    A handler for managing database schemas.

    This class provides methods to ensure that a schema exists in the database,
    creating it if necessary.
    """

    @staticmethod
    def create_table_schema(schema: str, db: Session) -> None:
        """
        Ensures that the specified schema exists in the database.

        If the schema does not exist, it will be created.

        Args:
            schema (str): The name of the schema to validate or create.
            db (Session): The SQLAlchemy database session used for execution.

        Raises:
            Exception: If an error occurs during schema creation.

        Note:
            This function should be used within a valid session scope.
        """

        with db.begin():
            stmt = f"CREATE SCHEMA IF NOT EXISTS {schema};"
            db.execute(text(stmt))
