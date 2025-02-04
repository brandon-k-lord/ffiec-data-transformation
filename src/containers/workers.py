from concurrent.futures import ProcessPoolExecutor

from .imports import ImportContainer
from .scripts import ScriptContainer


class WorkersContainer:
    def __init__(self, imports: ImportContainer, scripts: ScriptContainer):
        self._imports: ImportContainer = imports
        self._scripts: ScriptContainer = scripts

    def dependency(self):
        self._scripts.preflight_scripts()
        self._scripts.dependency_scripts()

    def import_workers(self):
        with ProcessPoolExecutor() as executer:
            executer.map(
                lambda func: func(),
                [
                    self._imports.attribute_import,
                    self._imports.relationship_import,
                    self._imports.transformation_import,
                    self._imports.gov_identifier_import,
                    self._imports.bhcf_import,
                ],
            )

    def script_workers(self):
        with ProcessPoolExecutor() as executer:
            executer.map(
                lambda func: func(),
                [
                    self._scripts.attribute_scripts,
                    self._scripts.relationship_scripts,
                    self._scripts.transformation_scripts,
                    self._scripts.gov_identifier_scripts,
                    self._scripts.call_report_scripts,
                ],
            )
