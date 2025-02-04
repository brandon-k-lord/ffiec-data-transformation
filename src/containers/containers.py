from sqlalchemy import Engine
from .configs import ConfigContainer
from .imports import ImportContainer
from ..handlers import FileHandler, ImportHandler
from ..database.connection import intit_engine
from ..constants.database import CONNECTION_STRING


class MasterContainer:
    def __init__(
        self, file_handler: FileHandler, import_handler: ImportHandler, engine: Engine
    ):
        self._file_handler: FileHandler = file_handler
        self._import_handler: ImportHandler = import_handler
        self._engine: Engine = engine

    def config_container(self) -> ConfigContainer:
        return ConfigContainer(
            file_handler=self._file_handler, import_handler=self._import_handler
        )

    def import_container(self) -> ImportContainer:
        return ImportContainer(
            config=self.config_container(),
            engine=self._engine,
            import_handler=self._import_handler,
        )


engine = intit_engine(connection_string=CONNECTION_STRING, echo=False)


def master_container() -> MasterContainer:
    return MasterContainer(
        engine=engine, file_handler=FileHandler, import_handler=ImportHandler
    )
