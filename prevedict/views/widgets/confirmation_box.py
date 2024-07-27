from PySide6.QtWidgets import QMessageBox

from prevedict.conf.ui_text import UIText


class ConfirmationBox(QMessageBox):
    def __init__(self, text: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle(UIText.CONFIRMATION)
        self.setText(text)
        self.confirm = self.addButton(UIText.CONFIRM, QMessageBox.AcceptRole)
        self.cancel = self.addButton(UIText.CANCEL, QMessageBox.RejectRole)
        self.setDefaultButton(self.buttons()[1])
        self.setEscapeButton(self.buttons()[1])

    def exec(self) -> bool:
        """
        Returns True if the action is confirmed, false, if it isn't.
        """
        super().exec()
        return self.clickedButton() == self.confirm
