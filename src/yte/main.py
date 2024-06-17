import sys
from PySide6.QtGui import QKeyEvent
from windows import SearchWindow

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QWidget,
    QSplitter,
)


class MainWindow(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("yte")
        self.setWindowFlags(
            Qt.WindowType.WindowMinimizeButtonHint
            | Qt.WindowType.WindowMaximizeButtonHint
            | Qt.WindowType.WindowCloseButtonHint
        )
        self.color = self.palette()
        self.color.setColor(self.backgroundRole(), "#282828")
        self.setPalette(self.color)

        self._splitter = QSplitter()
        self._splitter.setHandleWidth(0)

        self._search_window_toggled = True
        self._left = QWidget()
        self._right = QWidget()

        self._createApp()

    def _createApp(self):
        self.setLayout(self._createLayout())

    def _createLayout(self) -> QHBoxLayout:
        parent_layout = QHBoxLayout()
        search_window = SearchWindow()
        viewer_window = search_window._getViewerInstance()
        viewer_window_layout = viewer_window._createLayout()
        self._left.setLayout(search_window._createLayout())
        self._right.setLayout(viewer_window_layout)
        self._splitter.addWidget(self._left)
        self._splitter.addWidget(self._right)
        viewer_window.splitter = self._splitter
        parent_layout.addWidget(self._splitter)
        parent_layout.setContentsMargins(0, 0, 0, 0)
        return parent_layout

    def keyPressEvent(self, event: QKeyEvent) -> None:
        splitter_left_side = self._splitter.widget(0)

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
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main(app)
