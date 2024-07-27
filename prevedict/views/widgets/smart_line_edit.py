from PySide6.QtCore import QStringListModel, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QCompleter, QLineEdit


class SmartLineEdit(QLineEdit):
    shiftReturnPressed = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.completions = QStringListModel()
        ac = QCompleter(self.completions)
        ac.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setCompleter(ac)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
            self.shiftReturnPressed.emit()
        else:
            super().keyPressEvent(event)

    def set_autocomplete_text(self, text: str) -> None:
        pass
