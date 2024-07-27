from dataclasses import dataclass

from PySide6.QtGui import QFontDatabase


@dataclass
class FontWeight:
    name: str
    value: int


class FontInfo:
    """
    An abstraction over QFontDatabase that provides quick access to the available sizes
    and weights for a specific font by just passing its name to the constructor. It also
    provides a list of compatible fonts, i.e. fonts that have proper Cyrillic support
    and which can be scaled well.
    """

    _compatible_fonts = None

    def __init__(self, name: str) -> None:
        self.name = name
        self.sizes = QFontDatabase.pointSizes(self.name)
        self.weights = self._load_weights()

    def _load_weights(self) -> dict[int, str]:
        raw_styles = QFontDatabase.styles(self.name)
        weights = {}

        for style in raw_styles:
            font_weight = self._extract_weight_from_style(style)
            if not font_weight:
                continue
            weights[font_weight.value] = font_weight.name

        sorted = self._sort_weights(weights)
        return sorted

    def _extract_weight_from_style(self, style: str) -> FontWeight | None:
        for word in style.split():
            lowered = word.lower()
            if "condensed" in lowered:
                continue
            if "italic" in lowered:
                continue
            weight_int = QFontDatabase.weight(self.name, word)
            is_valid_weight = weight_int and weight_int > 0 and weight_int % 100 == 0
            if is_valid_weight:
                return FontWeight(word, weight_int)

    @staticmethod
    def _sort_weights(weights: dict[int, str]) -> dict[int, str]:
        weight_items = list(weights.items())
        weight_items.sort()
        return {value: name for value, name in weight_items}

    @classmethod
    def compatible_fonts(cls) -> list[str]:
        if cls._compatible_fonts:
            return cls._compatible_fonts

        fonts = QFontDatabase.families()

        with_cyrillic_support = []
        for font in fonts:
            if QFontDatabase.Cyrillic in QFontDatabase.writingSystems(font):
                with_cyrillic_support.append(font)

        properly_scalable = []
        for font in with_cyrillic_support:
            is_properly_scalable = len(QFontDatabase.pointSizes(font)) >= 10
            if is_properly_scalable:
                properly_scalable.append(font)

        cls._compatible_fonts = properly_scalable
        return cls._compatible_fonts
