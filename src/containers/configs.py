from typing import List
from ..constants import (
    FFIEC_BHCF_IMPORT,
    FFIEC_FI_IMPORT,
    IMPORT,
    SCRIPTS,
    SCRIPTS_PREFLIGHT,
    SCRIPTS_TRANS_LOAD,
)
from ..constants.dicts import FFEICConfig, ScriptsConfig

from ..handlers import ImportHandler, FileHandler


class ConfigContainer:
    def __init__(self, import_handler: ImportHandler, file_handler: FileHandler):
        self._import_handler: ImportHandler = import_handler
        self._file_handler: FileHandler = file_handler

    def bhcf_import_configs(self) -> List[FFEICConfig | ScriptsConfig]:
        return self._import_handler.create_config(
            configs=FFIEC_BHCF_IMPORT,
            directory=IMPORT,
            create_file_dict=self._file_handler.create_file_dict,
        )

    def fi_import_configs(self) -> List[FFEICConfig | ScriptsConfig]:
        return self._import_handler.create_config(
            configs=FFIEC_FI_IMPORT,
            directory=IMPORT,
            create_file_dict=self._file_handler.create_file_dict,
        )

    def preflight_script_configs(self) -> List[FFEICConfig | ScriptsConfig]:
        return self._import_handler.create_config(
            configs=SCRIPTS_PREFLIGHT,
            create_file_dict=self._file_handler.create_file_dict,
            directory=SCRIPTS,
        )

    def tranformation_script_configs(self) -> List[FFEICConfig | ScriptsConfig]:
        return self._import_handler.create_config(
            configs=SCRIPTS_TRANS_LOAD,
            create_file_dict=self._file_handler.create_file_dict,
            directory=SCRIPTS,
        )
