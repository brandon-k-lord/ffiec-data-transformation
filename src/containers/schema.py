"""
schema

This module defines the `SchemaContainer` class, which serves as a wrapper for managing 
database schema creation. It interacts with the `SchemaHandler` to define and create 
schemas asynchronously using SQLAlchemy.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from ..handlers import SchemaHandler
from ..constants import schema


class SchemaContainer:
    """
    A container class for managing schema-related operations.

    This class acts as an interface for handling schema creation using the `SchemaHandler`.

    Attributes:
        _schema_handler (SchemaHandler): An instance of `SchemaHandler` used for schema operations.
    """

    def __init__(self, schema_handler: SchemaHandler):
        """
        Initializes the SchemaContainer with a schema handler.

        Args:
            schema_handler (SchemaHandler): The handler responsible for managing schema creation.
        """
        self._schema_handler: SchemaHandler = schema_handler

    async def create_transformation_schema(
        self, db: AsyncSession, schema: str = schema.TRANSFORMATIONS
    ) -> None:
        """
        Creates the transformation schema in the database.

        This method uses the `SchemaHandler` to define the schema structure and execute
        schema creation asynchronously.

        Args:
            db (AsyncSession): The asynchronous database session.
            schema (str, optional): The name of the schema to create. Defaults to `schema.TRANSFORMATIONS`.

        Returns:
            None
        """
        return await self._schema_handler.create_table_schema(schema=schema, db=db)
