from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QPalette, QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow

from prevedict.conf import UIText, WinConfig, paths
from prevedict.conf.settings import Settings
from prevedict.utils import icon_drawer
from prevedict.views.main_view import MainView
from prevedict.views.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.define_shortcuts()

        self.main_view = MainView()
        self.main_view.settingsRequested.connect(self._show_settings)
        self.setCentralWidget(self.main_view)

        self.settings_view = None

        Settings.add_listener(self.configure)
        Settings.load()

    def configure(self, settings: Settings) -> None:
        self.settings = settings
        app: QApplication = QApplication.instance()
        app.setFont(settings.fonts.general.qfont)
        app.setPalette(settings.display.palette)
        self.setWindowTitle(UIText.MAIN_TITLE)
        self.load_icon(app)
        self.main_view.configure(settings)

    def load_icon(self, app: QApplication) -> None:
        color = self.settings.display.palette.color(QPalette.WindowText)
        icon = icon_drawer.draw_monochrome_icon(paths.APP_ICON, color)
        app.setWindowIcon(icon)

    ######################
    ### EVENT HANDLERS ###
    ######################
    def showEvent(self, event):
        self._load_win_config()
        super().showEvent(event)

    def closeEvent(self, event):
        self._save_win_config()
        super().closeEvent(event)

    def _show_settings(self) -> None:
        settings = SettingsDialog(self, self.settings)
        settings.open()

    def _load_win_config(self) -> None:
        wc = WinConfig.instance()
        mw = wc.main_window
        self.setGeometry(*mw.geometry)
        if mw.maximized:
            self.showMaximized()

    def _save_win_config(self) -> None:
        wc = WinConfig.instance()
        mw = wc.main_window
        s = wc.splitter

        mw.maximized = self.isMaximized()
        if not mw.maximized:
            geo = self.geometry()
            mw.geometry = [0, 0, geo.width(), geo.height()]

        s.proportions = self.main_view.splitter.sizes()
        wc.save()

    ################
    ### CONTROLS ###
    ################
    def define_shortcuts(self) -> None:
        self.quit = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.quit.activated.connect(self.close)

    def keyPressEvent(self, event) -> bool:
        """Re-implement key press event to route letter key presses to the input field."""
        key = event.key()
        if key == Qt.Key_Up:
            self._move_selection(-1)
            return True
        if key == Qt.Key_Down:
            self._move_selection(1)
            return True

        super().keyPressEvent(event)
        return True

    def _move_selection(self, offset) -> None:
        list_widget = self.main_view.list_widget
        current_row = list_widget.currentRow()
        current_count = list_widget.count()
        new_row = current_row + offset
        if new_row < 0:
            new_row = current_count + new_row
        if new_row >= current_count:
            new_row %= current_count
        list_widget.setCurrentRow(new_row)
