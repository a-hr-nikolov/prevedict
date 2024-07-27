from PySide6.QtWidgets import QSplitter


class Splitter(QSplitter):
    """
    A class that inherits from QSplitter, but calculates ratios to calculate the split,
    not specific pixel counts.
    """

    def __init__(
        self, orientation, proportions: list[int] = None, *args, **kwargs
    ) -> None:
        super().__init__(orientation, *args, **kwargs)
        self._proportions = proportions

    def set_proportions(self, proportions: list[int]) -> None:
        self._proportions = proportions
        self._resize()

    def _resize(self) -> None:
        if not self._proportions:
            return
        total_size = self.size().width()
        sum_prop = sum(self._proportions)
        sizes = [int(total_size * (prop / sum_prop)) for prop in self._proportions]
        self.setSizes(sizes)

    def resizeEvent(self, event):
        self._resize()
        super().resizeEvent(event)
