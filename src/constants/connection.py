"""
connection 

Defines connection strings for database access, using configuration settings.
"""

from config import settings

POSTGRES_CONNECTION = (
    f"{settings.db_driver}://{settings.db_usrnm}:{settings.db_pwd}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
