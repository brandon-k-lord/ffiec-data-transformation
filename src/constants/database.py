
from config import settings

CONNECTION_STRING=f"{settings.db_driver}://{settings.db_usrnm}:{settings.db_pwd}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
TRANSFORMATIONS_SCHEMA = "transformations"