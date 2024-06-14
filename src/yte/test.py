from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QHBoxLayout, QPushButton
import sys


def main():
    app = QApplication([])
    window = create_window()
    layout = create_layout(window)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec())


def create_layout(window: QWidget) -> QHBoxLayout:
    layout = QHBoxLayout()
    layout.addWidget(QPushButton("Click me!"))
    helloMsg = QLabel("<h1>Hello, World</h1>", parent=window)
    # set the position of welcome message
    helloMsg.move(60, 15)
    return layout


def create_window() -> QWidget:
    window = QWidget()
    window.setWindowTitle("A PyQt Application")
    window.setGeometry(100, 100, 280, 100)
    return window


if __name__ == "__main__":
    main()
