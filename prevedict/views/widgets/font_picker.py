from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from prevedict.utils import FontInfo


class FontPicker(QWidget):
    def __init__(self, label: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        label_widget = QLabel(label)
        font = label_widget.font()
        font.setBold(True)
        label_widget.setFont(font)
        vbox.addWidget(label_widget)

        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        self.font_list = FontInfo.compatible_fonts()

        ##########
        ### UI ###
        ##########
        self.names_combo = QComboBox()
        self.names_combo.addItems(self.font_list)
        self.names_combo.currentTextChanged.connect(self.on_selected_font)
        hbox.addWidget(self.names_combo)

        self.weights_combo = QComboBox()
        self.weights_combo.currentIndexChanged.connect(self.on_selected_weight)
        hbox.addWidget(self.weights_combo)

        self.sizes_combo = QComboBox()
        self.sizes_combo.currentIndexChanged.connect(self.on_selected_size)
        hbox.addWidget(self.sizes_combo)

    def on_selected_font(self, font_name: str) -> None:
        font_info = FontInfo(font_name)
        weights = font_info.weights
        self.weights_by_index = list(weights.items())
        current_weight = weights.get(self.weight_value, False)
        self._silent_set_combo(self.weights_combo, weights.values(), current_weight)

        self.sizes = [str(size) for size in font_info.sizes]
        self._silent_set_combo(self.sizes_combo, self.sizes, self.size_string)

        self.initial_data = self.data()

    def on_selected_weight(self, index) -> None:
        self.weight_value = self.weights_by_index[index][0]

    def on_selected_size(self, index) -> None:
        self.size_string = self.sizes[index]

    def data(self) -> dict[str]:
        name = self.names_combo.currentText()
        weight = self.weights_combo.currentText()
        size = int(self.sizes_combo.currentText())

        return {"name": name, "style": weight, "size": size}

    def set_font_selection(self, qfont: QFont) -> None:
        name = qfont.family()
        weight = qfont.weight()
        size = qfont.pointSize()

        self.initial_state = [name, weight, size]

        self.weight_value = (weight // 100) * 100
        self.size_string = str(size)
        self.names_combo.setCurrentText(name)

    @staticmethod
    def _silent_set_combo(combo: QComboBox, items: list[str], text: str) -> None:
        combo.blockSignals(True)
        combo.clear()
        combo.addItems(items)
        if text:
            combo.setCurrentText(text)
        combo.blockSignals(False)

    def has_changed(self) -> bool:
        if self.initial_data == self.data():
            return True
        return False
