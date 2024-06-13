import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMainWindow, QFrame, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class GameField(QWidget):
    def __init__(self, parent, is_own):
        super().__init__()
        self.initUI()
        self.parent = parent
        self.is_own = is_own  # Add a flag to indicate whether it's the own or enemy field
        if is_own:
            self.clicked_buttons = []  # Initialize an empty list to store clicked buttons for own field
        else:
            self.clicked_buttons = []  # Initialize an empty list to store clicked buttons for enemy field

    def initUI(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        for i in range(10):
            for j in range(10):
                button = QPushButton()  # Create an empty button
                button.setFixedSize(30, 30)  # Set the button size to 30x30
                button.clicked.connect(lambda checked, i=i, j=j, button=button: self.on_button_clicked(i, j, button))  # Connect the button click event
                grid_layout.addWidget(button, i, j)

    def on_button_clicked(self, i, j, button):
        if self.is_own:
            self.parent.clicked_buttons_own.append((i, j))  # Store the clicked button's position in the own field list
            print("Own field clicked:", self.parent.clicked_buttons_own)
        else:
            self.parent.clicked_buttons_enemy.append((i, j))  # Store the clicked button's position in the enemy field list
            print("Enemy field clicked:", self.parent.clicked_buttons_enemy)
            button.setStyleSheet("background-color: red")  # Change the button color to red

class ShipSelector(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ships = ["Ship 1", "Ship 2", "Ship 3", "Ship 4", "Ship 5"]
        self.current_ship = 0
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.ship_label = QPushButton(self.ships[self.current_ship])
        self.ship_label.setFixedSize(100, 30)
        layout.addWidget(self.ship_label)

        self.ship_preview = QWidget()
        self.ship_preview_layout = QVBoxLayout()
        self.ship_preview.setLayout(self.ship_preview_layout)
        layout.addWidget(self.ship_preview)

        button_layout = QHBoxLayout()
        prev_button = QPushButton("<")
        prev_button.setFixedSize(30, 30)
        prev_button.clicked.connect(self.prev_ship)
        button_layout.addWidget(prev_button)

        next_button = QPushButton(">")
        next_button.setFixedSize(30, 30)
        next_button.clicked.connect(self.next_ship)
        button_layout.addWidget(next_button)

        layout.addLayout(button_layout)

        self.update_ship_preview()

    def prev_ship(self):
        self.current_ship = (self.current_ship - 1) % len(self.ships)
        self.ship_label.setText(self.ships[self.current_ship])
        self.update_ship_preview()

    def next_ship(self):
        self.current_ship = (self.current_ship + 1) % len(self.ships)
        self.ship_label.setText(self.ships[self.current_ship])
        self.update_ship_preview()

    def update_ship_preview(self):
        while self.ship_preview_layout.count():
            child = self.ship_preview_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        ship_length = 2
        if self.current_ship == 1:
            ship_length = 3
        elif self.current_ship == 2:
            ship_length = 3
        elif self.current_ship == 3:
            ship_length = 4
        elif self.current_ship == 4:
            ship_length = 5
        for i in range(ship_length):
            button = QPushButton()
            button.setFixedSize(30, 30)
            self.ship_preview_layout.addWidget(button)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        self.clicked_buttons_own = []  # Initialize an empty list to store clicked buttons for own field
        self.clicked_buttons_enemy = []  # Initialize an empty list to store clicked buttons for enemy field

        left_layout = QVBoxLayout()
        self.ship_selector = ShipSelector(self)
        left_layout.addWidget(self.ship_selector)
        layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        game_field_layout = QHBoxLayout()
        right_layout.addLayout(game_field_layout)

        self.game_field1 = GameField(self, is_own=True)
        game_field_layout.addWidget(self.game_field1)

        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        game_field_layout.addWidget(separator)

        self.game_field2 = GameField(self, is_own=False)
        game_field_layout.addWidget(self.game_field2)

        layout.addLayout(right_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())