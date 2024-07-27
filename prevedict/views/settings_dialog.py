from dataclasses import dataclass

from pydantic import ValidationError
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from prevedict.conf import WinConfig
from prevedict.conf.settings import Font, Fonts, Lang, Settings
from prevedict.conf.ui_text import BiWord, UIText
from prevedict.views.widgets import ConfirmationBox, FontPicker, Tabs


class SettingsDialog(QDialog):
    def __init__(self, parent: QWidget, settings: Settings, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        self.settings = settings
        self.text = UIText
        self.setWindowTitle(self.text.SETTINGS_TITLE)

        self.disclaimer_text = self.text.FONT_DISCLAIMER

        self.font_pickers: dict[str, FontPicker] = dict.fromkeys(
            settings.fonts.get_targets()
        )

        self._init_UI()
        self.controller = SettingsController(self)
        self.controller.configure(settings)
        self._connect_handlers()

    def _init_UI(self) -> None:
        mainbox = QVBoxLayout()
        mainbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainbox)

        tabs = Tabs()
        tabs.setContentsMargins(*[0] * 4)
        mainbox.addWidget(tabs)

        general_tab = self._create_general_tab()
        tabs.addTab(general_tab, self.text.GENERAL_TAB)

        fonts_tab = self._create_fonts_tab()
        tabs.addTab(fonts_tab, self.text.FONTS_TAB)

        ##################
        ### OK, CANCEL ###
        ##################
        button_box = QHBoxLayout()
        mainbox.addLayout(button_box)

        self.restore_button = QPushButton()
        self.restore_button.setText(f"    {self.text.RESTORE_BUTTON}    ")

        button_box.addWidget(self.restore_button)

        button_box.addStretch(1)

        self.ok_button = QPushButton(self.text.OK)
        button_box.addWidget(self.ok_button)

        self.cancel_button = QPushButton(self.text.CANCEL)
        button_box.addWidget(self.cancel_button)

        button_box.setSpacing(5)
        button_box.setContentsMargins(*([10] * 4))

        self.cancel_button.setFocus()

    def _create_general_tab(self) -> QWidget:
        grid = QGridLayout()
        vbox = QVBoxLayout()
        tab = QWidget()

        vbox.addLayout(grid)
        tab.setLayout(vbox)

        self.language_combo = QComboBox()
        self.language_combo.addItems("")

        self.theme_combo = QComboBox()
        self.theme_combo.addItems("")

        self.words_spinbox = QSpinBox()
        self.words_spinbox.setRange(1, 100)

        labels = [self.text.LANGUAGE, self.text.THEME, self.text.LIST_LIMIT]
        widgets = [self.language_combo, self.theme_combo, self.words_spinbox]

        for i, (label, widget) in enumerate(zip(labels, widgets)):
            label_widget = QLabel(label + ":")
            label_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(label_widget, i, 0, Qt.AlignRight)
            grid.addWidget(widget, i, 1, Qt.AlignLeft)

        grid.setRowStretch(i + 1, 1)
        return tab

    def _create_fonts_tab(self) -> QWidget:
        font_box = QVBoxLayout()
        fonts_tab = QWidget()
        fonts_tab.setLayout(font_box)
        self.setLayout(font_box)

        fonts_disclaimer = QLabel(self.disclaimer_text)
        font_box.addWidget(fonts_disclaimer)
        for target in self.font_pickers:
            font_box.addSpacing(10)
            # This approach undoubtedly creates coupling, but it's the most convenient
            # and if it has to change, I will probably have to scrap the entire logic
            # here, so it wouldn't matter anyway.
            title = getattr(self.text, target.upper())
            picker = FontPicker(title)
            font_box.addWidget(picker)
            self.font_pickers[target] = picker

        font_box.addStretch(1)

        return fonts_tab

    def _connect_handlers(self) -> None:
        self.ok_button.clicked.connect(self.controller.on_ok)
        self.cancel_button.clicked.connect(self.controller.on_cancel)
        self.restore_button.clicked.connect(self.controller.on_restore)

    def _confirm_restore(self) -> None:
        mbox = ConfirmationBox(self.text.RESTORE_CONFIRMATION)
        response = mbox.exec()

        if response is True:
            self.controller.on_restore()

    def refresh(self) -> None:
        settings = self.parent().settings
        new = SettingsDialog(self.parent(), settings)
        self.close()
        new.open()


class SettingsController:
    def __init__(self, gui: SettingsDialog) -> None:
        self.gui = gui
        self.current_state: "SettingsData" = None

    def configure(self, settings: Settings) -> None:
        self.list_limit = settings.behavior.list_limit
        self.theme = settings.display.theme
        self.language = settings.display.language
        self.fonts = settings.fonts
        self.settings = settings

        self.language_words = [UIText.EN, UIText.BG]
        self.theme_words = [UIText.DEFAULT, UIText.LIGHT, UIText.DARK]

        self.init_gui_state()

        self.current_data = self.extract_data()

    def init_gui_state(self) -> None:
        lang_idx = self.get_initial_index(self.language_words, self.language)
        theme_idx = self.get_initial_index(self.theme_words, self.theme)

        self.gui.language_combo.addItems(self.language_words)
        self.gui.language_combo.setCurrentIndex(lang_idx)

        self.gui.theme_combo.addItems(self.theme_words)
        self.gui.theme_combo.setCurrentIndex(theme_idx)

        self.gui.words_spinbox.setValue(self.list_limit)

        for target, picker in self.gui.font_pickers.items():
            target_font: Font = getattr(self.fonts, target)
            qfont = target_font.qfont
            picker.set_font_selection(qfont)

    def on_ok(self) -> None:
        data = self.extract_data()
        has_changed = self.current_data != data
        if not has_changed:
            self.gui.close()
            return

        self.update_user_settings(data)
        self.gui.close()

    def on_cancel(self) -> None:
        data = self.extract_data()
        has_changed = self.current_data != data
        if not has_changed:
            self.gui.close()
            return

        confirmed = self.get_confirmation(UIText.SETTINGS_CANCEL_CONFIRMATION)
        if not confirmed:
            return
        self.gui.close()

    def on_restore(self) -> None:
        confirmed = self.get_confirmation(UIText.RESTORE_CONFIRMATION)
        if not confirmed:
            return

        WinConfig.restore_defaults()
        self.settings.restore_defaults()
        self.gui.refresh()

    def extract_data(self) -> "SettingsData":
        language_idx = self.gui.language_combo.currentIndex()
        theme_idx = self.gui.theme_combo.currentIndex()
        list_limit = self.gui.words_spinbox.value()
        fonts_data = self.extract_fonts_data()

        return SettingsData(
            language_index=language_idx,
            theme_index=theme_idx,
            list_limit=list_limit,
            fonts_data=fonts_data,
        )

    def extract_fonts_data(self) -> dict[str]:
        picker_items = self.gui.font_pickers.items()
        return {font: picker.data() for font, picker in picker_items}

    def update_user_settings(self, data: "SettingsData") -> None:
        try:
            self.settings.display.language = Lang(
                self.language_words[data.language_index].en
            )
            self.settings.display.theme = self.theme_words[data.theme_index].en
            self.settings.behavior.list_limit = data.list_limit
            self.settings.fonts = Fonts(**data.fonts_data)
        except ValidationError:
            # Implement an invalid settings popup
            mb = QMessageBox()
            mb.setWindowTitle(UIText.NOTIFICATION_TITLE)
            mb.setText(UIText.INVALID_SETTINGS_NOTIFICATION)
            mb.addButton(UIText.OK, QMessageBox.AcceptRole)
            mb.exec()
            self.settings.silent_load()
            return

        self.settings.save()

    @staticmethod
    def get_initial_index(ls: list[BiWord], val: str) -> int:
        standardized = [word.en for word in ls]
        return standardized.index(val)

    @staticmethod
    def get_confirmation(text: str) -> bool:
        cb = ConfirmationBox(text)
        return cb.exec()


@dataclass
class SettingsData:
    language_index: int
    theme_index: int
    list_limit: int
    fonts_data: dict[str, dict[str]]
