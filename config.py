from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_driver: str
    db_usrnm: str
    db_pwd: str
    db_host: str
    db_port: str
    db_name: str

    class Config:
        env_file = ".env"


settings = Settings()
