from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile


def helper_create_profile(
    profile_name: str, _browser: QWebEngineView
) -> QWebEngineProfile:
    browser_profile = QWebEngineProfile(profile_name, _browser)
    browser_profile.setHttpUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
    )
    browser_profile.setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies
    )
    return browser_profile
