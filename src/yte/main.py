import sys
from pathlib import PurePath

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QDialog, QStatusBar, QToolBar, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QSplitter
from PyQt6.QtWebEngineWidgets import QWebEngineView


class SearchWindow:
    def __init__(self):
        self._browser = QWebEngineView()
        self._browser.setUrl(QUrl("https://www.youtube.com/"))

    def _createMenuBar(self) -> QToolBar:
        navbar = QToolBar("Navigation")
        # back button
        back_button = QAction(
            QIcon(str(PurePath(r"icons").joinpath("arrow-180.png"))), "Back", parent=self._browser)
        # connects a signal (back_button.triggered) to a function slot (self._browser.back)
        # 'back' is a function but we put the callback to it for now, which will only be run if the button 'back_button' is pressed
        back_button.triggered.connect(self._browser.back)
        navbar.addAction(back_button)
        # forward button
        back_button = QAction(
            QIcon(str(PurePath(r"icons").joinpath("arrow-000.png"))), "Forward", parent=self._browser)
        back_button.triggered.connect(self._browser.forward)
        navbar.addAction(back_button)
        return navbar

    def _createLayout(self):
        search_window_layout = QVBoxLayout()
        search_window_navbar = self._createMenuBar()
        search_window_layout.addWidget(search_window_navbar)
        search_window_layout.addWidget(self._browser)
        return search_window_layout


class ViewerWindow:
    def __init__(self):
        self.window = QWidget()


class MainWindow(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("yte")
        self._createApp()

    def _createApp(self):
        self.setLayout(self._createLayout())

    def _createLayout(self) -> QHBoxLayout:
        parent_layout = QHBoxLayout()
        search_window_layout = SearchWindow()._createLayout()
        parent_layout.addLayout(search_window_layout)
        return parent_layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
