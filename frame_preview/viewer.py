from .viewer_tk import *


class Viewer:
    def __init__(self):
        self._window = None

    def show_image(self, num):
        if not self._is_open():
            self._create_window()
        self._window.show(num)

    def _is_open(self):
        if self._window is None:
            return False
        if not self._window.winfo_exists():
            return False
        return True

    def _create_window(self):
        self._window = ViewerTk()
