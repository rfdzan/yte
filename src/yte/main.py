import sys
from pathlib import PurePath

from PySide6.QtCore import QUrl, QStandardPaths
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QDialog,
    QStatusBar,
    QToolBar,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QSplitter,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage


class CustomWebPage(QWebEnginePage):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def acceptNavigationRequest(
        self, url: QUrl, type: QWebEnginePage.NavigationType, isMainFrame: bool
    ) -> bool:
        # seems like requestedUrl() is what I need.
        print(self.requestedUrl().toString())
        # print(
        #     QStandardPaths().writableLocation(
        #         QStandardPaths().StandardLocation.GenericDataLocation
        #     )
        # )
        # if it returns True, loads the requested url
        # else, it won't load

        # PLAN:
        # read requestedUrl(), if it matches regex, do not load the page on SearchWindow, instead open it to side with the url changed to embed. <- i already have this regex
        return True


class CustomWebView(QWebEngineView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setPage(CustomWebPage(self))


class SearchWindow:
    def __init__(self):
        self._browser = CustomWebView()
        self._browser.setUrl(QUrl("https://www.youtube.com/"))

    def _createMenuBar(self) -> QToolBar:
        navbar = QToolBar("Navigation")
        # back button
        back_button = QAction(
            QIcon(str(PurePath(r"icons").joinpath("arrow-180.png"))),
            "Back",
            parent=self._browser,
        )
        # connects a signal (back_button.triggered) to a function slot (self._browser.back)
        # 'back' is a function but we put the callback to it for now, which will only be run if the button 'back_button' is pressed
        back_button.triggered.connect(self._browser.back)
        navbar.addAction(back_button)
        # forward button
        back_button = QAction(
            QIcon(str(PurePath(r"icons").joinpath("arrow-000.png"))),
            "Forward",
            parent=self._browser,
        )
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
        self._browser = QWebEngineView()
        self._browser.load("https://www.google.com/")

    def _createLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.addWidget(self._browser)
        return layout

    def loadPage(self, url: str):
        self._browser.load(QUrl(url))


class MainWindow(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("yte")
        self._left = QWidget()
        self._right = QWidget()
        self._createApp()

    def _createApp(self):
        self.setLayout(self._createLayout())

    def _createLayout(self) -> QHBoxLayout:
        splitter = QSplitter()
        parent_layout = QHBoxLayout()
        search_window_layout = SearchWindow()._createLayout()
        viewer_window_layout = ViewerWindow()._createLayout()
        self._left.setLayout(search_window_layout)
        self._right.setLayout(viewer_window_layout)
        splitter.addWidget(self._left)
        splitter.addWidget(self._right)
        parent_layout.addWidget(splitter)
        return parent_layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
