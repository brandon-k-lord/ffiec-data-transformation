from sqlalchemy.ext.asyncio import AsyncSession

from ..handlers.schema import SchemaHandler
from ..constants import schemas


class SchemaContainer:
    def __init__(self, schema_handler: SchemaHandler):
        self._schema_handler: SchemaHandler = schema_handler

    async def create_transformation_schema(
        self, db: AsyncSession, schema: str = schemas.TRANSFORMATIONS
    ) -> None:
        return await self._schema_handler.create_table_schema(schema=schema, db=db)
