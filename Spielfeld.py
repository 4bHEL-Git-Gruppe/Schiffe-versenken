import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMainWindow, QFrame, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel

class GameField(QWidget):
    def __init__(self, parent, is_own):
        super().__init__()
        self.parent = parent
        self.is_own = is_own
        self.buttons = [[None for _ in range(10)] for _ in range(10)]
        self.clicked_buttons = []
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)
        for i in range(10):
            for j in range(10):
                button = QPushButton()
                button.setFixedSize(30, 30)
                button.clicked.connect(lambda checked, i=i, j=j: self.on_button_clicked(i, j))
                layout.addWidget(button, i, j)
                self.buttons[i][j] = button

    def on_button_clicked(self, i, j):
        if (i, j) in self.clicked_buttons:
            msg_box = QMessageBox()
            msg_box.setText("Button already clicked!")
            msg_box.exec_()
            return
        if self.is_own:
            ship_selector = self.parent.ship_selector
            if ship_selector.current_ship < len(ship_selector.ships):
                ship_type = ship_selector.current_ship
                ship_lengths = [2, 3, 3, 4, 5]  # hardcoded ship lengths
                ship_length = ship_lengths[ship_type]
                color = ["blue", "green", "yellow", "orange", "red"][ship_type]  # subtract 1 from current_ship
                orientation = self.ask_orientation()
                if orientation == "horizontal":
                    can_place_ship = True
                    for k in range(ship_length):
                        if j + k >= 10:
                            can_place_ship = False
                            break
                        if self.is_adjacent_occupied(i, j + k):
                            can_place_ship = False
                            break
                    if can_place_ship:
                        for k in range(ship_length):
                            self.buttons[i][j + k].setStyleSheet(f"background-color: {color}")
                            self.clicked_buttons.append((i, j + k))
                        ship_selector.next_ship()  # Call next_ship method
                    else:
                        print("Ship cannot be placed next to another ship!")
                elif orientation == "vertical":
                    can_place_ship = True
                    for k in range(ship_length):
                        if i + k >= 10:
                            can_place_ship = False
                            break
                        if self.is_adjacent_occupied(i + k, j):
                            can_place_ship = False
                            break
                    if can_place_ship:
                        for k in range(ship_length):
                            self.buttons[i + k][j].setStyleSheet(f"background-color: {color}")
                            self.clicked_buttons.append((i + k, j))
                        ship_selector.next_ship()  # Call next_ship method
                    else:
                        print("Ship cannot be placed next to another ship!")
            else:
                print("All ships placed!")
        else:
            self.parent.clicked_buttons_enemy.append((i, j))
            print("Enemy field clicked:", self.parent.clicked_buttons_enemy)
            self.buttons[i][j].setStyleSheet("background-color: red")

    def ask_orientation(self):
        msg_box = QMessageBox()
        msg_box.setText("Choose orientation:")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.button(QMessageBox.Yes).setText("Horizontal")
        msg_box.button(QMessageBox.No).setText("Vertical")
        ret = msg_box.exec_()
        if ret == QMessageBox.Yes:
            return "horizontal"
        else:
            return "vertical"

    def is_adjacent_occupied(self, i, j):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if 0 <= i + x < 10 and 0 <= j + y < 10:
                    if (i + x, j + y) in self.clicked_buttons:
                        return True
        return False

class ShipSelector(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ships = ["Ship 1", "Ship 2", "Ship 3", "Ship 4", "Ship 5"]
        self.current_ship = 0  # Initialize to 0, will increment when a ship is placed
        self.ship_lengths = [2, 3, 3, 4, 5]
        self.ship_colors = ["blue", "green", "yellow", "orange", "red"]
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

        self.update_ship_preview()

    def update_ship_preview(self):
        while self.ship_preview_layout.count():
            child = self.ship_preview_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        if self.current_ship < len(self.ships):
            ship_length = self.ship_lengths[self.current_ship]
            ship_color = self.ship_colors[self.current_ship]
            for i in range(ship_length):
                button = QPushButton()
                button.setFixedSize(30, 30)
                button.setStyleSheet(f"background-color: {ship_color}")
                self.ship_preview_layout.addWidget(button)
        else:
            self.ship_preview.hide()  # Hide the ship preview when all ships are placed
            label = QLabel("All ships placed!")
            self.ship_preview_layout.addWidget(label)

    def next_ship(self):
        self.current_ship += 1
        if self.current_ship < len(self.ships):
            self.ship_label.setText(self.ships[self.current_ship])
            self.update_ship_preview()
        else:
            self.ship_label.hide()  # Hide the ship label
            self.ship_preview.hide()  # Hide the ship preview
            start_game_button = QPushButton("Ready")
            start_game_button.setFixedSize(100, 30)
            self.layout().addWidget(start_game_button)  # Add button to main layout
            start_game_button.clicked.connect(self.start_game)  # Connect to start_game method

    def start_game(self):
        start_game_button = self.sender()  # Get the button that was clicked
        start_game_button.setStyleSheet("background-color: green")  # Turn button green
        print("Ready!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        self.clicked_buttons_own = []
        self.clicked_buttons_enemy = []

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