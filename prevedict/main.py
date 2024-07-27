import sys

from PySide6.QtWidgets import QApplication

from prevedict.views.main_window import MainWindow


class App(QApplication):
    def __init__(self) -> None:
        super().__init__(sys.argv)

    def run(self) -> None:
        self.main_window = MainWindow()
        self.main_window.show()


def main():
    app = App()
    app.run()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
