from PySide6.QtCore import Qt, QThreadPool, QTimer, Signal
from PySide6.QtWidgets import QListWidget, QVBoxLayout, QWidget

from prevedict.conf import UIText, WinConfig, paths
from prevedict.conf.settings import Settings
from prevedict.model.dictionary import Dictionary, WordTranslation
from prevedict.model.thesaurus import Thesaurus, WordDescription
from prevedict.utils.worker import Worker
from prevedict.views.info_dialog import InfoDialog
from prevedict.views.widgets import (
    FixedHBoxLayout,
    IconButton,
    SmartLineEdit,
    Splitter,
    WordDisplay,
)


class MainView(QWidget):
    settingsRequested = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.settings_icon_path = str(paths.SETTINGS_ICON)
        self._init_UI()

        self.controller = MainController(self)

    def configure(self, settings: Settings) -> None:
        self.settings = settings

        self.input_field.setFont(settings.fonts.input.qfont)
        self.input_field.setPlaceholderText(UIText.INPUT_PLACEHOLDER)
        self.list_widget.setFont(settings.fonts.word_list.qfont)

        ### PASS ON ###
        self.controller.configure(settings)
        self.description.configure(settings)
        self.settings_button.configure(settings)
        self.info_button.configure(settings)

        ### SPLITTER ###
        s = WinConfig.instance().splitter
        self.splitter.set_proportions(s.proportions)

    def _init_UI(self) -> None:
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        hbox = FixedHBoxLayout()
        vbox.addLayout(hbox)

        self.input_field = SmartLineEdit()
        hbox.addWidget(self.input_field)

        self.settings_button = IconButton(paths.SETTINGS_ICON)
        hbox.addWidget(self.settings_button)

        self.info_button = IconButton(paths.INFO_ICON)
        hbox.addWidget(self.info_button)

        self.splitter = Splitter(Qt.Orientation.Horizontal)
        vbox.addWidget(self.splitter)

        self.list_widget = QListWidget()
        self.splitter.addWidget(self.list_widget)

        self.description = WordDisplay()
        self.splitter.addWidget(self.description)

    #################
    ### INTERFACE ###
    #################
    def get_selected_text(self, row: int) -> str:
        return self.list_widget.item(row).text()

    def update_list(self, items: list[str]) -> None:
        if not items:
            return
        self.list_widget.clear()
        self.list_widget.addItems(items)
        self._silent_set_to_first_row()

    def _silent_set_to_first_row(self) -> None:
        self.list_widget.blockSignals(True)
        self.list_widget.setCurrentRow(0)
        self.list_widget.blockSignals(False)

    def focus_input(self) -> None:
        self.input_field.setFocus()

    def show_info(self):
        info = InfoDialog(self, self.settings)
        info.show()


class MainController:
    def __init__(self, gui: MainView) -> None:
        self.gui = gui
        self.dict: Dictionary = None
        self.thesaurus = Thesaurus
        self.thread_pool = QThreadPool()

        self._connect_handlers()
        self._lazy_load_dict()

    def configure(self, settings: Settings) -> None:
        self.list_limit = settings.behavior.list_limit

    def _lazy_load_dict(self) -> None:
        def inner():
            self.dict = Dictionary()

        QTimer.singleShot(1, inner)

    ######################
    ### EVENT HANDLERS ###
    ######################
    def _connect_handlers(self):
        self.gui.input_field.textChanged.connect(self.handle_input)
        self.gui.input_field.returnPressed.connect(self.handle_input_enter)
        self.gui.input_field.shiftReturnPressed.connect(self.handle_input_shift_enter)
        self.gui.list_widget.currentRowChanged.connect(self.handle_list_selection)
        self.gui.settings_button.clicked.connect(self.gui.settingsRequested.emit)
        self.gui.info_button.clicked.connect(self.gui.show_info)

    def handle_input(self, input: str) -> None:
        completions = self.get_completions(input)
        if not completions:
            return
        word_translation = self.get_word_translation(completions[0])
        self.display_word_details(word_translation)
        self.gui.update_list(completions)

    def handle_list_selection(self, row: int) -> None:
        if row < 0:
            return
        selection = self.gui.get_selected_text(row)
        word_translation = self.get_word_translation(selection)
        self.display_word_details(word_translation)

    def handle_input_enter(self) -> None:
        text = self.gui.input_field.text()
        matches = self.dict.find_best_matches(text, self.list_limit)
        if not matches:
            return
        word_translation = self.get_word_translation(matches[0])
        self.display_word_details(word_translation)
        self.gui.update_list(matches)

    def handle_input_shift_enter(self) -> None:
        self.gui.list_widget.clear()
        self.gui.description.display_loading()
        text = self.gui.input_field.text()

        worker = Worker(self.thesaurus.get, text)
        worker.returned.connect(self.update_description)
        self.thread_pool.start(worker)

    ########################
    ### VIEW INTERACTION ###
    ########################
    def display_word_details(self, word) -> None:
        self.gui.description.display(word)

    def update_description(self, details: WordDescription | None) -> None:
        if not details:
            self.gui.description.display_not_found()
            return
        self.display_word_details(details)

    #########################
    ### MODEL INTERACTION ###
    #########################
    def get_word_translation(self, text: str) -> WordTranslation:
        return self.dict.get(text)

    def get_completions(self, word: str) -> list[str]:
        candidates = self.dict.list_word_completions(word, self.list_limit)
        return candidates

    @classmethod
    def get_description_from_word_details(cls, word_details: WordDescription) -> str:
        descriptions = []

        for meaning in word_details.meanings:
            definitions = []

            for i, definition in enumerate(meaning.definitions, 1):
                definitions.append(f"{i}. {definition.definition}")

            def_str = "\n".join(definitions)

            lines = [
                f"({meaning.partOfSpeech.lower()}) ",
                f"{def_str}",
            ]
            if meaning.synonyms:
                lines.append(f"=== [SIMILAR]: {", ".join(meaning.synonyms)}")

            descriptions.append("\n".join(lines))

        return "\n\n".join(descriptions)
