from constants import (
    BROWSER_STORAGE_PATH,
    BROWSER_PERSISTENT_STORAGE,
    BROWSER_STORAGE_DOWNLOAD,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings


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
    browser_profile.settings().setAttribute(
        QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
    )
    browser_profile.settings().setAttribute(
        QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True
    )
    browser_profile.settings().setAttribute(
        QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True
    )

    browser_profile.setCachePath(str(BROWSER_STORAGE_PATH))
    browser_profile.setDownloadPath(str(BROWSER_STORAGE_DOWNLOAD))
    # persistentStorage is the problem, YT search page won't load

    # discrepancy:
    # - self-created path does not inclue 'Local Storage' and 'Session Storage' folders <- these two were by default under this folder naming scheme:

    # '/home/user/.local/share/main.py/QtWebEngine/profile_name'

    # browser_profile.setPersistentStoragePath(
    #     str(BROWSER_PERSISTENT_STORAGE.joinpath(profile_name))
    # )
    print(browser_profile.persistentStoragePath())
    return browser_profile
