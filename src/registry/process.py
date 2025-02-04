from ..containers.workers import WorkersContainer


class ProcessRegistry:
    """
    A class responsible for managing and executing worker processes.

    This class acts as a centralized process registry that coordinates the execution
    of dependencies, import operations, and script execution.

    Attributes:
        _workers (WorkersContainer): An instance of `WorkersContainer` that manages
                                     import and script execution workflows.
    """

    def __init__(self, workers: WorkersContainer) -> None:
        """
        Initializes the ProcessRegistry with a `WorkersContainer` instance.

        Parameters:
            workers (WorkersContainer): The container responsible for handling import
                                        and script execution tasks.
        """
        self._workers: WorkersContainer = workers

    def process(self) -> None:
        """
        Executes the full process pipeline by triggering dependency setup, import tasks,
        and script execution in the correct order.
        """
        self._workers.dependency()
        self._workers.import_workers()
        self._workers.script_workers()
