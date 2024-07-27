from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap


def draw_monochrome_icon(icon_path: Path, color: QColor) -> QIcon:
    pixmap = QPixmap(icon_path)

    transparent_map = QPixmap(pixmap.size())
    transparent_map.fill(Qt.transparent)

    painter = QPainter(transparent_map)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.fillRect(pixmap.rect(), color)
    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    return QIcon(transparent_map)
