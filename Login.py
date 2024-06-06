import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QGridLayout,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(64, 64, 255))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        # app.setPalette(palette)  # This should be set on the QApplication, not the QMainWindow
        
        layout = QGridLayout()

        # Passwort Lineedit 
        pwd = QLineEdit()
        pwd.setEchoMode(QLineEdit.EchoMode.Password)
        pwd.setFixedSize(100, 30)
        pwd.setStyleSheet("QLineEdit { background : transparent; }") 
        
        layout.addWidget(pwd, 0, 2)

        # Eingabefeld Label
        eingabe_feld = QLabel("Password:")
        eingabe_feld.setStyleSheet("QLabel { color : rgb(0,0,0); }")
        eingabe_feld.setFixedSize(70, 30)
        layout.addWidget(eingabe_feld, 0, 1)

        # Test Label
        test = QLabel("Test Label")
        test.setStyleSheet("background-color : rgb(10,10,10); color: white;")
        test.setFixedSize(100, 100)
        layout.addWidget(test, 3, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
stylesheet = """
QMainWindow {
    background-image: url(login_bild2.jpg);
    background-repeat: no-repeat;
    background-position: center;
}
"""
app.setStyleSheet(stylesheet)
w = MainWindow()
w.setStyleSheet(stylesheet)
w.resize(870, 500)
w.show()
app.exec()