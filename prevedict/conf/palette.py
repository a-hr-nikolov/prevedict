from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


class Palette:
    __default = None

    @classmethod
    def default(cls) -> QPalette:
        cls.__default = (
            cls.__default if cls.__default else QApplication.instance().palette()
        )

        return cls.__default

    @classmethod
    def light(cls) -> QPalette:
        app: QApplication = QApplication.instance()
        if not cls.__default:
            cls.__default = app.palette()

        light_palette = app.palette()
        light_palette.setColor(QPalette.Window, QColor(220, 220, 220))
        light_palette.setColor(QPalette.WindowText, Qt.black)
        light_palette.setColor(
            QPalette.Disabled, QPalette.WindowText, QColor(160, 160, 160)
        )
        light_palette.setColor(QPalette.Base, QColor(240, 240, 240))
        light_palette.setColor(QPalette.AlternateBase, QColor(230, 230, 230))
        light_palette.setColor(QPalette.ToolTipBase, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ToolTipText, Qt.black)
        light_palette.setColor(QPalette.Text, Qt.black)
        light_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(160, 160, 160))
        light_palette.setColor(QPalette.Dark, QColor(200, 200, 200))
        light_palette.setColor(QPalette.Shadow, QColor(150, 150, 150))
        light_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ButtonText, Qt.black)
        light_palette.setColor(
            QPalette.Disabled, QPalette.ButtonText, QColor(160, 160, 160)
        )
        light_palette.setColor(QPalette.BrightText, QColor(80, 80, 80))
        light_palette.setColor(QPalette.Link, QColor(0, 122, 255))
        light_palette.setColor(QPalette.Highlight, QColor(60, 60, 60))
        light_palette.setColor(
            QPalette.Disabled, QPalette.Highlight, QColor(190, 190, 190)
        )
        light_palette.setColor(QPalette.HighlightedText, Qt.white)
        light_palette.setColor(
            QPalette.Disabled,
            QPalette.HighlightedText,
            QColor(160, 160, 160),
        )
        light_palette.setColor(QPalette.PlaceholderText, QColor(140, 140, 140))

        return light_palette

    @classmethod
    def dark(cls) -> QPalette:
        app: QApplication = QApplication.instance()
        if not cls.__default:
            cls.__default = app.palette()

        dark_palette = app.palette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(
            QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127)
        )
        dark_palette.setColor(QPalette.Base, QColor(32, 32, 32))
        dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Dark, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.Shadow, QColor(20, 20, 20))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(
            QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127)
        )
        dark_palette.setColor(QPalette.BrightText, QColor(180, 180, 180))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        dark_palette.setColor(
            QPalette.Disabled,
            QPalette.HighlightedText,
            QColor(127, 127, 127),
        )
        dark_palette.setColor(QPalette.PlaceholderText, QColor(140, 140, 140))

        return dark_palette
