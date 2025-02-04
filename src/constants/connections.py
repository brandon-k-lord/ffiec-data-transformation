from config import settings


POSTGRES_CONNECTION = f"{settings.db_driver}://{settings.db_usrnm}:{settings.db_pwd}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
