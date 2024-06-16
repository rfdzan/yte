import re
from PySide6.QtCore import QObject, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import (
    QWebEnginePage,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)


def do_navigate(msg: str) -> bool:
    pattern_long = (
        r"(\w+://www\.)(youtube\.com/)(?:watch|live)(\W(?:v=)?[^\?]+)(?:\W\w+=.+)?"
    )
    matches_long = re.match(pattern_long, msg, re.IGNORECASE)
    if matches_long is None:
        return True
    print(f"navigate url matches {matches_long.groups()}")
    return False


def convert_to_embed(msg: str) -> QUrl | None:
    domain = "https://www.youtube.com/embed/"
    pattern_long = (
        r"(\w+://www\.)(youtube\.com/)(?:watch|live)(\W(?:v=)?[^\?]+)(?:\W\w+=.+)?"
    )
    pattern_video_id = r"\W\w=([\w-]+)"
    matches_long = re.match(pattern_long, msg, re.IGNORECASE)
    if matches_long is None:
        return matches_long
    video_id = re.match(pattern_video_id, matches_long.group(3), re.IGNORECASE)
    return QUrl(domain + video_id.group(1))


class URLInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, p: QObject | None = ...) -> None:
        super().__init__(p)

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        print(info)


class CustomWebPage(QWebEnginePage):
    from windows import ViewerWindow

    def __init__(self, parent=None, viewer_window=ViewerWindow) -> None:
        super().__init__(parent)
        self._viewer = viewer_window
        self.setUrlRequestInterceptor(URLInterceptor(self))
        # self.navigationRequested.connect(self.load_embed)
        self.linkHovered.connect(self.load_embed)

    def load_embed(self, url: QUrl):
        # to_str = url if isinstance(url, str) else url.toString()
        # navigate_to = self.requestedUrl().toString()
        update_url = convert_to_embed(url)
        if update_url is not None:
            self._viewer.url = update_url

    # def acceptNavigationRequest(
    #     self, url: QUrl | str, type: QWebEnginePage.NavigationType, isMainFrame: bool
    # ) -> bool:
    #     # print("acceptNavigationRequest is called.")
    #     # to_str = url if isinstance(url, str) else url.toString()
    #     navigate_to = self.requestedUrl().toString()
    #     if QWebEnginePage.NavigationType.NavigationTypeLinkClicked:
    #         # to_open = url if isinstance(url, QUrl) else QUrl(url)
    #         self._viewer._loadUrl(url=convert_to_embed(navigate_to))

    #     # PLAN:
    #     # read requestedUrl(), if it matches regex, do not load the page on SearchWindow, instead open it to side with the url changed to embed. <- i already have this regex
    #     should_navigate = do_navigate(navigate_to)
    #     return should_navigate


class CustomWebView(QWebEngineView):
    from windows import ViewerWindow

    def __init__(self, viewer_window: ViewerWindow, parent=None) -> None:
        super().__init__(parent)
        self._viewer = viewer_window
        self._page = CustomWebPage(self, viewer_window=self._viewer)
        self.setPage(self._page)
