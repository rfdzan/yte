import sys
import typing
from PySide6.QtGui import QKeyEvent, QResizeEvent
from windows import SearchWindow

from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QWidget,
    QSplitter,
)


class MainWindow(QDialog):
    def __init__(self, screens: list[QScreen]):
        super().__init__(parent=None)
        self.setWindowTitle("yte")
        self.setWindowFlags(
            Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self._screens = screens
        self.searchWindow = SearchWindow()

        self._layout = QHBoxLayout()
        self._splitter = QSplitter()

        self._left = QWidget()
        self._right = QWidget()

        self._createApp(
            self._createLayout,
            self._setMainWindowColor,
            self._createLeftRightWindows,
            self._createSplitter,
        )
        self._search_window_toggled = True
        self._toggle_window_switch = False

    def _createApp(
        self,
        mainLayout: typing.Callable[[], QHBoxLayout],
        setColors: typing.Callable[[], None],
        leftRightWindows: typing.Callable[[], tuple[QWidget, QWidget]],
        splitter: typing.Callable[[QWidget, QWidget], None],
    ):
        layout = mainLayout()
        setColors()
        leftRightWindows()
        splitter(self._left, self._right)
        layout.addWidget(self._splitter)

    def _setMainWindowColor(self):
        self.color = self.palette()
        self.color.setColor(self.backgroundRole(), "#282828")
        self.setPalette(self.color)

    def _createLeftRightWindows(self) -> tuple[QWidget, QWidget]:
        self._left.setLayout(self.searchWindow._createLayout())
        self._right.setLayout(self.searchWindow.viewerInstance._createLayout())

    def _createSplitter(self, left: QWidget, right: QWidget):
        self._splitter.setHandleWidth(0)
        self._splitter.addWidget(left)
        self._splitter.addWidget(right)
        self.searchWindow.viewerInstance.splitter = self._splitter

    def _createLayout(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        return layout

    def _windowSwitching(self, switch: bool):
        orientation = Qt.Orientation.Vertical if switch else Qt.Orientation.Horizontal
        right = self._right if switch else self._left
        self._splitter.setOrientation(orientation)
        right.setParent(None)
        left = self._splitter.replaceWidget(0, right)
        self._splitter.addWidget(left)

    def resizeEvent(self, resize: QResizeEvent) -> None:
        # TODO: tweak `activeMonitor` so the window can detect which screen its in.
        activeMonitor = self._screens[0]
        maxWidth = activeMonitor.size().width()
        currentWidth = resize.size().width()
        if currentWidth <= maxWidth // 2 and not self._toggle_window_switch:
            self._toggle_window_switch = True
            self._windowSwitching(True)

        if currentWidth > maxWidth // 2 and self._toggle_window_switch:
            self._toggle_window_switch = False
            self._windowSwitching(False)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        splitter_left_side = self._splitter.widget(
            1 if self._toggle_window_switch else 0
        )
        if event.key() != Qt.Key.Key_T:
            return
        if self._search_window_toggled:
            splitter_left_side.hide()
            self._search_window_toggled = False
            return
        if not self._search_window_toggled:
            splitter_left_side.show()
            self._search_window_toggled = True
            return


def main(app: QApplication):
    window = MainWindow(app.screens())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main(app)
