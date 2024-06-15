import sys
from windows import SearchWindow

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
        self._left = QWidget()
        self._right = QWidget()
        self._createApp()

    def _createApp(self):
        self.setLayout(self._createLayout())

    def _createLayout(self) -> QHBoxLayout:
        splitter = QSplitter()
        parent_layout = QHBoxLayout()
        search_window = SearchWindow()
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
