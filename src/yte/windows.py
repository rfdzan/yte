from pathlib import PurePath


from PySide6.QtCore import QUrl
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QToolBar, QHBoxLayout, QVBoxLayout, QSplitter
from PySide6.QtWebEngineWidgets import QWebEngineView


class ViewerWindow:
    def __init__(self):
        self._browser = QWebEngineView()
        self._splitter = None
        self._browser.load("https://www.google.com/")

    def _set_splitter(self, splitter: QSplitter):
        self._splitter = splitter

    def _getInstance(self) -> QWebEngineView:
        return self._browser

    def _check_splitter_toggle(self, hide_search_window: QAction):
        splitter_left_side = self._splitter.widget(0)
        if hide_search_window:
            print("hide search window: active")
            splitter_left_side.hide()

        else:
            print("hide search window: inactive")
            splitter_left_side.show()

    def _createLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        navbar = QToolBar()
        hide_search_window = QAction(
            QIcon(str(PurePath(r"icons").joinpath("arrow-180.png"))),
            "Back",
            parent=self._browser,
        )
        hide_search_window.setCheckable(True)
        hide_search_window.triggered.connect(self._check_splitter_toggle)
        navbar.addAction(hide_search_window)

        layout.addWidget(navbar)
        layout.addWidget(self._browser)
        return layout

    def _getUrl(self):
        return self._browser.url().toString()

    def _loadUrl(self, url: QUrl):
        print(f"_loadUrl is called on: {url.toString()}")
        self._browser.setUrl(url)

    url = property(fset=_loadUrl, fget=_getUrl)
    splitter = property(fset=_set_splitter)


class SearchWindow:
    def __init__(self):
        from custom_webengine import CustomWebView

        self._viewer = ViewerWindow()
        self._browser = CustomWebView(self._viewer)
        self._browser.setUrl(QUrl("https://www.youtube.com/"))

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
