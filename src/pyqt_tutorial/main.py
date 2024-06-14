import sys


from PyQt6.QtWidgets import QApplication, QLabel, QDialog, QStatusBar, QToolBar, QHBoxLayout, QWidget, QPushButton


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


class MainWindow(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        self._createApp()

    def _createApp(self):
        self.setLayout(self._createLayout())

    def _createLayout(self) -> QHBoxLayout:
        parent_layout = QHBoxLayout()
        search_window = SearchWindow().createWidget()
        viewer_window = ViewerWindow()
        parent_layout.addWidget(search_window)
        return parent_layout


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
