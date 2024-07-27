from enum import Enum
from typing import Annotated, Callable, ClassVar

from pydantic import BaseModel, Field
from PySide6.QtGui import QFont, QPalette

from prevedict.conf import defaults, helpers, paths
from prevedict.conf.palette import Palette
from prevedict.utils import QFontConstructor


class Lang(str, Enum):
    BG = "Bulgarian"
    EN = "English"


class Theme(str, Enum):
    DEFAULT = "Default"
    DARK = "Dark"
    LIGHT = "Light"


class Font(BaseModel, validate_assignment=True):
    name: str
    style: str
    size: Annotated[int, Field(ge=6, le=72)]
    _qfont: QFontConstructor = None

    @property
    def qfont(self) -> QFont:
        if self._qfont:
            return self._qfont

        self._qfont = QFontConstructor.create(self.name, self.style, self.size)
        return self._qfont


class Behavior(BaseModel, validate_assignment=True):
    list_limit: Annotated[int, Field(ge=1, le=100)]


class Display(BaseModel):
    language: Lang
    theme: Theme

    @property
    def palette(self) -> QPalette:
        return getattr(Palette, self.theme.lower())()


class Fonts(BaseModel):
    general: Font
    input: Font
    heading: Font
    transcription: Font
    word_list: Font

    def get_targets(self) -> list[str]:
        return list(dict(self).keys())


class Settings(BaseModel):
    behavior: Behavior
    display: Display
    fonts: Fonts
    __callbacks: ClassVar[list[Callable[["Settings"], None]]] = []

    @classmethod
    def load(cls) -> "Settings":
        settings = cls.silent_load()
        settings.__notify()
        return settings

    @classmethod
    def silent_load(cls) -> "Settings":
        from_json = helpers.load_from_json(paths.SETTINGS)
        merged = helpers.merge_dicts(defaults.SETTINGS, from_json)
        return cls(**merged)

    def save(self) -> None:
        current = self.model_dump()
        to_dump = helpers.get_updated_subset_keys(defaults.SETTINGS, current)
        if not to_dump:
            helpers.dump_to_json({}, paths.SETTINGS)

        dumped = self.model_dump(include=to_dump)
        helpers.dump_to_json(dumped, paths.SETTINGS)
        self.__notify()

    @classmethod
    def restore_defaults(cls) -> None:
        helpers.dump_to_json({}, paths.SETTINGS)
        cls.load()

    @classmethod
    def add_listener(cls, callback: Callable[["Settings"], None]) -> None:
        cls.__callbacks.append(callback)

    def __notify(self) -> None:
        for cb in self.__callbacks:
            cb(self)
