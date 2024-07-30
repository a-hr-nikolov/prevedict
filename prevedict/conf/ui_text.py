from prevedict.conf.settings import Lang, Settings


class BiWord(str):
    _lang: Lang = None

    def __new__(cls, en: str, bg: str, *args, **kwargs):
        value = en if cls._lang == Lang.EN else bg
        return super().__new__(cls, value, *args, **kwargs)

    def __init__(self, en: str, bg: str) -> None:
        self.en = en
        self.bg = bg


class UIText:
    @staticmethod
    def __update(settings: Settings):
        BiWord._lang = settings.display.language
        UIText.__init()

    Settings.add_listener(__update)

    @classmethod
    def __init(cls) -> None:
        cls.MAIN_TITLE = BiWord(
            "Prevedict",
            "Prevedict",
        )

        cls.SETTINGS_TITLE = cls.MAIN_TITLE + BiWord(
            " - Settings",
            " - Настройки",
        )

        cls.INPUT_PLACEHOLDER = BiWord(
            "Enter a word...",
            "Въведи дума...",
        )

        cls.FONT_DISCLAIMER = BiWord(
            "NOTE: Listing only automatically selected compatible fonts.",
            "ВАЖНО: Показват се само автоматично подбрани съвместими шрифтове.",
        )

        cls.THEME = BiWord(
            "Theme",
            "Тема",
        )

        cls.LIST_LIMIT = BiWord(
            "Listed words limit",
            "Макс. предложени думи",
        )

        cls.GENERAL_TAB = BiWord(
            "General",
            "Основни",
        )

        cls.FONTS_TAB = BiWord(
            "Fonts",
            "Шрифтове",
        )

        cls.OK = BiWord(
            "OK",
            "Приеми",
        )

        cls.CANCEL = BiWord(
            "Cancel",
            "Откажи",
        )

        cls.CONFIRM = BiWord(
            "Confirm",
            "Потвърди",
        )

        cls.THEME = BiWord(
            "Theme",
            "Тема",
        )

        cls.DARK = BiWord(
            "Dark",
            "Тъмна",
        )

        cls.LIGHT = BiWord(
            "Light",
            "Светла",
        )

        cls.LANGUAGE = BiWord(
            "Language",
            "Език",
        )

        cls.DEFAULT = BiWord(
            "Default",
            "По подразбиране",
        )

        cls.HEADING = BiWord(
            "Heading",
            "Заглавие",
        )

        cls.TRANSCRIPTION = BiWord(
            "Transcription",
            "Транскрипция",
        )

        cls.INPUT = BiWord(
            "Input",
            "Поле за въвеждане",
        )

        cls.WORD_LIST = BiWord(
            "Word List",
            "Списък с Думи",
        )

        cls.GENERAL = BiWord(
            "General",
            "Основен",
        )

        cls.EN = BiWord(
            "English",
            "Английски",
        )

        cls.BG = BiWord(
            "Bulgarian",
            "Български",
        )

        cls.EXPORT_BUTTON = BiWord(
            "Export settings",
            "Запази настройките във файл",
        )

        cls.IMPORT_BUTTON = BiWord(
            "Import settings",
            "Зареди настройки от файл",
        )

        cls.RESTORE_BUTTON = BiWord(
            "Restore defaults",
            "Възстанови началните настройки...",
        )

        cls.CONFIRMATION = BiWord(
            "Confirmation",
            "Потвърждение",
        )

        cls.RESTORE_CONFIRMATION = BiWord(
            "This action overrides the current settings and is not reversible. Do you wish to continue?",
            "Това действие презаписва настоящите настройки и не е обратимо. Искате ли да продължите?",
        )

        cls.SETTINGS_CANCEL_CONFIRMATION = BiWord(
            "All changes you have made will be discarded. Do you wish to continue?",
            "Направените промени ще бъдат отхвърлени. Желаете ли да продължите?",
        )

        cls.NOTIFICATION_TITLE = BiWord(
            "Notification",
            "Уведомление",
        )

        cls.INVALID_SETTINGS_NOTIFICATION = BiWord(
            "Invalid values detected. The changes will not be applied.",
            "Засечени са невалидни стойности. Промените няма да бъдат запазени.",
        )

        cls.LOADING = BiWord(
            "Loading thesaurus entry, please wait...",
            "Зарежда се информация от тълковен речник, моля почакайте...",
        )

        cls.NOT_FOUND = BiWord(
            en=(
                "Cannot find a matching word."
                "\n\nPossible reasons:"
                "\n  • Invalid or Cyrillic characters in search query"
                "\n    (thesaurus available in English only)"
                "\n  • Long search query with unresolvable spelling errors"
                "\n  • No approximate word matches exist in the database"
                "\n  • Connection with the thesaurus server cannot be established"
            ),
            bg=(
                "Не е намерена такава дума."
                "\n\Възможни причини:"
                "\n  • Невалидни символи или кирилица в заявката за търсене"
                "\n    (тълковеният речник е достъпен само за английски думи)"
                "\n  • Дълга заявка с правописни грешки, които не могат да бъдат поправени"
                "\n  • Не съществуват близки до заявката думи в базата данни"
                "\n  • Не може да се осъществи интернет връзка със сървъра"
            ),
        )

        cls.CLOSE = BiWord(
            "Close",
            "Затвори",
        )

        cls.INSTRUCTIONS_TITLE = BiWord(
            "Instructions",
            "Инструкции",
        )

        cls.KEYBINDINGS = BiWord(
            "Keybindings",
            "Клавишни функции",
        )
