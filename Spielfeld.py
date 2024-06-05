import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QPushButton

class GameField(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        for i in range(10):
            for j in range(10):
                button = QPushButton()  # Create an empty button
                button.setFixedSize(30, 30)  # Set the button size to 30x30
                grid_layout.addWidget(button, i, j)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout()
        central_widget.setLayout(layout)

        game_field1 = GameField()
        game_field2 = GameField()
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)

        layout.addWidget(game_field1, 0, 0)
        layout.addWidget(separator, 0, 1)
        layout.addWidget(game_field2, 0, 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())