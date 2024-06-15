import sys
from pathlib import PurePath
from dataclasses import dataclass

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


class ViewerWindow:
    def __init__(self):
        self._browser = QWebEngineView()
        self._browser.load("https://www.google.com/")

    def _getInstance(self) -> QWebEngineView:
        return self._browser

    def _createLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.addWidget(self._browser)
        return layout

    def _getUrl(self):
        return self._browser.url().toString()

    def _loadUrl(self, url: str):
        print("_loadUrl is called.")
        self._browser.setUrl(QUrl(url))

    url = property(fset=_loadUrl, fget=_getUrl)


class CustomWebPage(QWebEnginePage):
    def __init__(self, parent=None, viewer_window=ViewerWindow) -> None:
        super().__init__(parent)
        self._viewer = viewer_window

    def acceptNavigationRequest(
        self, url: QUrl, type: QWebEnginePage.NavigationType, isMainFrame: bool
    ) -> bool:
        # seems like requestedUrl() is what I need.
        print(self.requestedUrl().toString())
        self._viewer.url = self.requestedUrl().toString()
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
    def __init__(self, viewer_window: ViewerWindow, parent=None) -> None:
        super().__init__(parent)
        self._viewer = viewer_window
        self._page = CustomWebPage(self, viewer_window=self._viewer)
        self.setPage(self._page)


class SearchWindow:
    def __init__(self):
        self._viewer = ViewerWindow()
        self._browser = CustomWebView(self._viewer)
        self._browser.setUrl(QUrl("https://www.youtube.com/"))
        # TODO: control ViewerWindow from SearchWindow.

    def _getViewerInstance(self) -> ViewerWindow:
        return self._viewer

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
        forward_button = QAction(
            QIcon(str(PurePath(r"icons").joinpath("arrow-000.png"))),
            "Forward",
            parent=self._browser,
        )
        forward_button.triggered.connect(self._browser.forward)
        navbar.addAction(forward_button)
        return navbar

    def _createLayout(self):
        search_window_layout = QVBoxLayout()
        search_window_navbar = self._createMenuBar()
        search_window_layout.addWidget(search_window_navbar)
        search_window_layout.addWidget(self._browser)
        return search_window_layout


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
        search_window = SearchWindow()
        # search_window_layout = seach._createLayout()
        viewer_window_layout = search_window._getViewerInstance()._createLayout()
        self._left.setLayout(search_window._createLayout())
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
