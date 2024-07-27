import time
import unittest
from unittest.mock import patch

from PySide6.QtCore import QTimer


class TestApp(unittest.TestCase):
    @patch("sys.exit")
    def test_app_starts_and_closes_immediately(self, mock_exit):
        # fmt: off
        import_start = time.perf_counter()  # noqa: E402
        from prevedict.main import App, MainWindow  # noqa: E402
        import_duration = time.perf_counter() - import_start  # noqa: E402
        # fmt: on

        app_init = time.perf_counter()
        app = App()
        app_init_duration = time.perf_counter() - app_init

        with patch.object(app, "exec", return_value=0):
            # Patch the `show` method of QMainWindow to insert the QTimer call
            with patch.object(MainWindow, "show", self.patched_show(MainWindow)):
                start = time.perf_counter()
                app.run()
        open_close_duration = time.perf_counter() - start

        total_launch_time = import_duration + app_init_duration + open_close_duration
        print("############################")
        print(f"Launch Time: {total_launch_time:0.3f} seconds")
        print("############################")

    def patched_show(self, obj):
        original_show = obj.show

        def new_show(main_window):
            original_show(main_window)
            # Insert the QTimer.singleShot call to close the main window immediately
            QTimer.singleShot(0, main_window.close)

        return new_show


if __name__ == "__main__":
    unittest.main()
