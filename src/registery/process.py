from ..containers.workers import WorkersContainer


class ProcessRegistery:
    def __init__(self, workers: WorkersContainer):
        self._workers: WorkersContainer = workers

    def process_registery(self) -> None:
        self._workers.dependency()
        self._workers.import_workers()
        self._workers.script_workers()
