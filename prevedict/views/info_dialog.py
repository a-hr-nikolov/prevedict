from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from prevedict.conf import paths
from prevedict.conf.settings import Settings
from prevedict.conf.ui_text import UIText


class InfoDialog(QDialog):
    def __init__(self, parent, settings: Settings, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.setWindowTitle(UIText.INSTRUCTIONS_TITLE)
        self.setMinimumSize(560, 500)
        self.lang = settings.display.language.value
        self.colors = settings.display.palette

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        text = self.create_text_edit()
        vbox.addWidget(text)

        close_button = QPushButton()
        close_button.setText(UIText.CLOSE)
        close_button.clicked.connect(self.close)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(close_button)

        vbox.addLayout(hbox)

    def get_label_text(self) -> str:
        lines = self.extract_translation()
        return self.process_lines(lines)

    def extract_translation(self) -> list[str]:
        with open(paths.INFO_TEXT, encoding="UTF-8") as text:
            lines = text.readlines()

        start_index = lines.index(f"[{self.lang}]\n")
        end_index = lines.index("===\n", start_index + 1)

        return lines[start_index + 1 : end_index]

    def process_lines(self, lines: list[str]) -> str:
        joined = (
            f"<h2><b>{UIText.KEYBINDINGS}</b></h2><p><i>{lines[0].strip("\n")}</i></p>"
        )
        lines = lines[1:]
        processed = []

        for line in lines:
            col_index = line.find("]") + 1
            keybind = f"<b>{line[:col_index]}</b>"
            description = line[col_index:]
            whole = f"<p>{keybind.strip()}<br/>{description.strip()}</p>"
            processed.append(whole)

        return joined + "".join(processed)

    def create_text_edit(self) -> QTextEdit:
        text = QTextEdit(self.get_label_text())
        text.setReadOnly(True)
        return text
