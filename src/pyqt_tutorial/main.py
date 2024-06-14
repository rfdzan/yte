import sys
from pathlib import PurePath

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QDialog, QStatusBar, QToolBar, QHBoxLayout, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView


class SearchWindow:
    def __init__(self):
        self._browser = QWebEngineView()
        self._browser.setUrl(QUrl("https://www.youtube.com/"))

    def createWidget(self) -> QWebEngineView:
        return self._browser

    def _createMenuBar(self, browser: QWebEngineView):
        navbar = QToolBar("Navigation")
        # back button
        back_button = QAction(
            QIcon(str(PurePath(r"icons").joinpath("arrow-180.png"))), "Back", parent=browser)
        back_button.triggered.connect(self._browser.back)
        navbar.addAction(back_button)
        # forward button
        back_button = QAction(
            QIcon(str(PurePath(r"icons").joinpath("arrow-000.png"))), "Forward", parent=self._browser)
        back_button.triggered.connect(self._browser.forward)
        navbar.addAction(back_button)
        return navbar


class ViewerWindow:
    def __init__(self):
        self.window = QWidget()


class MainWindow(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        self._createApp()

    def _createApp(self):
        self.setLayout(self._createLayout())

    def _createLayout(self) -> QHBoxLayout:
        parent_layout = QVBoxLayout()
        search_window = SearchWindow()
        create_search_browser = search_window.createWidget()
        search_window_navbar = search_window._createMenuBar(
            create_search_browser)
        parent_layout.addWidget(search_window_navbar)
        parent_layout.addWidget(create_search_browser)
        return parent_layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
