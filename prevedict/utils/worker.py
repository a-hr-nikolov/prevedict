from typing import Any, Callable

from PySide6.QtCore import QObject, QRunnable, Signal


class WorkerSignals(QObject):
    returned = Signal(object)
    finished = Signal()


class Worker(QRunnable):
    def __init__(self, fn: Callable[..., Any], *args, **kwargs) -> None:
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.__signals = WorkerSignals()
        self.returned = self.__signals.returned
        self.finished = self.__signals.finished

    def run(self) -> None:
        result = self.fn(*self.args, **self.kwargs)
        self.returned.emit(result)
        self.finished.emit()
