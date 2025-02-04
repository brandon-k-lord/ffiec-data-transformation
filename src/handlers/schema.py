from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SchemaHandler:

    @staticmethod
    async def create_table_schema(schema: str, db: AsyncSession) -> None:
        """
        Ensures table schema exists

        Parameters:
        - schema: name of schema for validation/creation
        - engine: connection
        """

        async with db.begin():
            stm = f"create schema if not exists {schema};"
            await db.execute(text(stm))
            await db.commit()
