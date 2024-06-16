import sys
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
        self._left = QWidget()
        self._right = QWidget()
        self._createApp()

    def _createApp(self):
        self.setLayout(self._createLayout())

    def _createLayout(self) -> QHBoxLayout:
        splitter = QSplitter()
        parent_layout = QHBoxLayout()
        search_window = SearchWindow()
        viewer_window = search_window._getViewerInstance()
        viewer_window_layout = viewer_window._createLayout()
        self._left.setLayout(search_window._createLayout())
        self._right.setLayout(viewer_window_layout)
        splitter.addWidget(self._left)
        splitter.addWidget(self._right)
        viewer_window.splitter = splitter
        parent_layout.addWidget(splitter)
        return parent_layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
