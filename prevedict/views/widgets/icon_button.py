from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QPushButton

from prevedict.conf.settings import Settings
from prevedict.utils.icon_drawer import draw_monochrome_icon


class IconButton(QPushButton):
    def __init__(self, icon_path: Path, *args, **kwargs) -> None:
        """
        The anchor argument takes a QWidget and anchors the size of the IconButton to
        that widget. This involves a lot of ugly logic, but it is what it is.
        """
        super().__init__(*args, **kwargs)
        self.icon_path = icon_path

    def configure(self, settings: Settings) -> None:
        color = settings.display.palette.color(QPalette.PlaceholderText)
        icon = draw_monochrome_icon(self.icon_path, color)
        self.setIcon(icon)

    def set_size(self, size: int) -> None:
        self.setFixedSize(size, size)
        self.setIconSize(QSize(size * 0.8, size * 0.8))
