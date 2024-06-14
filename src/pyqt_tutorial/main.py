import sys
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QStatusBar, QToolBar, QHBoxLayout, QWidget, QPushButton


class SearchWindow:
    def __init__(self):
        ...

    def createWidget(self) -> QPushButton:
        # example
        button = QPushButton("Click me!")
        return button


class ViewerWindow:
    def __init__(self):
        self.window = QWidget()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        self.main_window = QWidget()
        self._createApp()

    def _createApp(self):
        self._createMenu()
        self._createStatusBar()
        self.main_window.setLayout(self._createLayout())
        self.setCentralWidget(self.main_window)

    def _createLayout(self) -> QHBoxLayout:
        parent_layout = QHBoxLayout()
        search_window = SearchWindow().createWidget()
        viewer_window = ViewerWindow()
        parent_layout.addWidget(search_window)
        return parent_layout

    def _createMenu(self):
        # adding '&' -> allows keyboard shortcuts
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("&Exit", self.close)
        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
