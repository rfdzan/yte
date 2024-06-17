import re
from global_helper import helper_create_profile
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile


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


class CustomWebPage(QWebEnginePage):
    from windows import ViewerWindow

    def __init__(
        self, parent=None, profile=QWebEngineProfile, viewer_window=ViewerWindow
    ) -> None:
        super().__init__(profile, parent)
        self._viewer = viewer_window
        self.linkHovered.connect(self.load_embed)

    def load_embed(self, url: QUrl):
        update_url = convert_to_embed(url)
        if update_url is not None:
            self._viewer.url = update_url


class CustomWebView(QWebEngineView):
    from windows import ViewerWindow

    def __init__(self, viewer_window: ViewerWindow, parent=None) -> None:
        super().__init__(parent)
        self._viewer = viewer_window
        self._page = CustomWebPage(
            parent=self,
            viewer_window=self._viewer,
            profile=helper_create_profile("search", self),
        )
        self.setPage(self._page)
