from PySide6.QtWidgets import QStackedWidget, QTabBar, QVBoxLayout, QWidget


class Tabs(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        self.tab_bar = QTabBar()
        self.tab_bar.currentChanged.connect(self.on_tab_change)
        vbox.addWidget(self.tab_bar)

        self.stack = QStackedWidget()
        self.stack.setContentsMargins(20, 20, 20, 20)
        vbox.addWidget(self.stack)

    def addTab(self, widget: QWidget, title: str) -> None:
        self.tab_bar.addTab(title)
        self.stack.addWidget(widget)

    def on_tab_change(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
