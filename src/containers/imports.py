from sqlalchemy import Engine
from .configs import ConfigContainer
from ..handlers import ImportHandler


class ImportContainer:

    def __init__(
        self, config: ConfigContainer, import_handler: ImportHandler, engine: Engine
    ):
        self._config: ConfigContainer = config
        self._import_handler: ImportHandler = import_handler
        self._engine: Engine = engine

    def bhcf_import(self) -> None:
        configs = self._config.bhcf_import_configs()
        return self._import_handler.import_handler(
            configs=configs,
            engine=self._engine,
            import_loader=self._import_handler.import_loader,
        )

    def fi_import(self) -> None:
        configs = self._config.fi_import_configs()
        return self._import_handler.import_handler(
            configs=configs,
            engine=self._engine,
            import_loader=self._import_handler.import_loader,
        )

    def preflight_script(self) -> None:
        configs = self._config.preflight_script_configs()
        return self._import_handler.import_handler(
            configs=configs,
            engine=self._engine,
            import_loader=self._import_handler.import_loader,
        )

    def transformation_script(self) -> None:
        configs = self._config.tranformation_script_configs()
        return self._import_handler.import_handler(
            configs=configs,
            engine=self._engine,
            import_loader=self._import_handler.import_loader,
        )
