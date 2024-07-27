from typing import Protocol

from PySide6.QtWidgets import QHBoxLayout, QWidget


class Sizeable(Protocol):
    def set_size(size: int) -> None: ...


class FixedHBoxLayout(QHBoxLayout):
    """
    A special case of QHBoxLayout, which gets its height fixed to the height of the
    first added widget.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__children: list[Sizeable] = []
        self.__first: QWidget = None

    def __autosize(self, event) -> None:
        self.__first.__class__.resizeEvent(self.__first, event)
        if len(self.__children) == 0:
            return

        height = self.__first.height()
        for child in self.__children:
            child.set_size(height)

    def addWidget(self, widget: QWidget) -> None:
        if not self.__first:
            self.__first = widget
            self.__first.resizeEvent = self.__autosize
        else:
            self.__children.append(widget)
        super().addWidget(widget)
