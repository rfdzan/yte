from PySide6.QtCore import QUrl

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

class CustomWebPage(QWebEnginePage):
    from windows import ViewerWindow
    def __init__(self, parent=None, viewer_window=ViewerWindow) -> None:
        super().__init__(parent)
        self._viewer = viewer_window

    def acceptNavigationRequest(
        self, url: QUrl | str, type: QWebEnginePage.NavigationType, isMainFrame: bool
    ) -> bool:

        self._viewer.url = self.requestedUrl().toString()
        # PLAN:
        # read requestedUrl(), if it matches regex, do not load the page on SearchWindow, instead open it to side with the url changed to embed. <- i already have this regex
        return True


class CustomWebView(QWebEngineView):
    from windows import ViewerWindow
    def __init__(self, viewer_window: ViewerWindow, parent=None) -> None:
        super().__init__(parent)
        self._viewer = viewer_window
        self._page = CustomWebPage(self, viewer_window=self._viewer)
        self.setPage(self._page)