from .containers import handler_container, HandlerContainer


class WorkersContainer:
    def __init__(self, handler_container: HandlerContainer):
        self._handler_container: HandlerContainer = handler_container
