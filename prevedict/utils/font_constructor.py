from PySide6.QtGui import QFont, QFontDatabase

from prevedict.conf import const


class QFontConstructor:
    _default_name = const.DEFAULT_FONT_NAME
    _default_path = const.DEFAULT_FONT_PATH
    __initialized = False

    @classmethod
    def create(cls, name: str, style: str, size: int) -> QFont:
        if not QFontDatabase.hasFamily(name):
            name = cls._default_name
            cls._load_default()

        qfont = QFontDatabase.font(name, style, size)
        return qfont

    @classmethod
    def _load_default(cls) -> None:
        if cls.__initialized or cls._default_name in QFontDatabase.families():
            return
        font_id = QFontDatabase.addApplicationFont(cls._default_path)
        if font_id == -1:
            print("Default font couldn't load.")
        cls.__initialized = True

    @staticmethod
    def scale(font: QFont, scale: float) -> QFont:
        font = QFont(font)
        scaled_size = round(font.pointSize() * scale)
        font.setPointSize(scaled_size)
        return font
