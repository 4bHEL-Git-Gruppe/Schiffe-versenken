import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QGridLayout,
    QPushButton,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setFixedSize(870, 500)
        self.create_ui()
        
        self.signup.clicked.connect(self.signup_clicked)
    
    def create_ui(self):
        # Login/Register
        main_layout = QGridLayout()
        vert_layout = QVBoxLayout()
        hort1_layout = QHBoxLayout()
        hort2_layout = QHBoxLayout()
        hort3_layout = QHBoxLayout()
        horb_layout = QHBoxLayout()

        # Top

        # Hintergrund Label
        hintergrund_top = QLabel("")
        hintergrund_top.setStyleSheet("background-color : rgba(40,40,40, 70); "
                                      "border : 2px solid grey;"
                                      "border-radius: 10%;")
        hintergrund_top.setFixedSize(530, 115)
        
        # Vertical 1
        # Anweisungen 
        anweisung_label = QLabel("Gib hier deine Daten ein: ")
        anweisung_label.setStyleSheet("QLabel { color : rgb(255,255,255); "
                                    "font-size : 18pt;"
                                    "border : 2px solid rgba(255,255,255,80);"
                                    "border-radius: 10%;"
                                    "}")
        anweisung_label.setFixedSize(280, 35)

        hort1_layout.addWidget(anweisung_label)
        vert_layout.addLayout(hort1_layout)

        # Vertical 2
        # Username Label
        username_label = QLabel("Username:")
        username_label.setStyleSheet("QLabel { color : rgb(255,255,255); "
                                     "font-size : 12pt;"
                                     "}")
        username_label.setFixedSize(80, 30)
        hort2_layout.addWidget(username_label)

        # Username Lineedit 
        username = QLineEdit()
        username.setFixedSize(100, 30)
        username.setStyleSheet("QLineEdit { background : transparent;" 
                          "border : 1px solid black;"
                          "border-radius: 5%;}") 
        hort2_layout.addWidget(username)
        vert_layout.addLayout(hort2_layout)

        # Vertical 3
        # Password Label
        password_label = QLabel("Password:")
        password_label.setStyleSheet("QLabel { color : rgb(255,255,255); "
                                     "font-size : 12pt;"
                                     "}")
        password_label.setFixedSize(80, 30)
        hort3_layout.addWidget(password_label)

        # Passwort Lineedit 
        pwd = QLineEdit()
        pwd.setEchoMode(QLineEdit.EchoMode.Password)
        pwd.setFixedSize(100, 30)
        pwd.setStyleSheet("QLineEdit { background : transparent;" 
                          "border : 1px solid black;"
                          "border-radius: 5%;}") 
        hort3_layout.addWidget(pwd)
        vert_layout.addLayout(hort3_layout)

        # Bottom
        hintergrund_bottom = QLabel("")
        hintergrund_bottom.setStyleSheet("background-color : rgba(40,40,40, 70); "
                           "border : 2px solid grey;"
                           "border-radius: 10%;")
        hintergrund_bottom.setFixedSize(530, 110)

        welcome = QLabel("Ey Kamerad, willst du dich ")
        welcome.setStyleSheet("font-size : 14pt")
        welcome.setFixedSize(220, 35)
        horb_layout.addWidget(welcome)

        self.signup = QPushButton("Einloggen")
        self.signup.setStyleSheet("font-size : 14pt")
        self.signup.setFixedSize(110, 35)
        horb_layout.addWidget(self.signup)

        oder = QLabel("oder")
        oder.setStyleSheet("font-size : 14pt")
        oder.setFixedSize(40, 35)
        horb_layout.addWidget(oder)

        register = QPushButton("Registrieren")
        register.setStyleSheet("font-size : 14pt")
        register.setFixedSize(120, 35)
        horb_layout.addWidget(register)        

        # Set spacing and margins to reduce distance between widgets
        hort1_layout.setSpacing(0)  
        hort1_layout.setContentsMargins(40, 3, 0, 0)

        hort2_layout.setSpacing(5)  
        hort2_layout.setContentsMargins(180, 0, 150, 0)

        hort3_layout.setSpacing(5)  
        hort3_layout.setContentsMargins(180, 0, 150, 0)

        vert_layout.setSpacing(5)  
        vert_layout.setContentsMargins(0, 0, 0, 0)

        horb_layout.setSpacing(5)  
        horb_layout.setContentsMargins(10, 0, 0, 37)

        # Hinzufügen der Widgets zum Hauptlayout
        main_layout.addWidget(hintergrund_top, 0, 0, Qt.AlignmentFlag.AlignTop)
        main_layout.addLayout(vert_layout, 0, 0, Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(hintergrund_bottom, 2, 0, Qt.AlignmentFlag.AlignBottom)
        main_layout.addLayout(horb_layout, 2, 0, Qt.AlignmentFlag.AlignBottom)

        main_layout.setRowStretch(2, 1)
        main_layout.setContentsMargins(0,10,1,10)

        # central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

        # background image
        self.setStyleSheet("""
            QMainWindow {
                background-image: url(login_bild2.jpg);
                background-position: center;
                background-repeat: no-repeat;
            }
        """)
    
    def signup_clicked(self):
        # Entferne das zentrale Widget
        self.central_widget.setParent(None)
        # Erstelle die neue UI
        self.create_client()
        
    def create_client(self):
        # Setze den Hintergrund auf eine andere Farbe
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgb(230,230,230)
            }
        """)
        # Hier kannst du die UI für den Client-Bereich erstellen
        client_ver_layout = QVBoxLayout()
        client_hort_layout = QHBoxLayout()
        client_label = QLabel("Welcome to the client area!")
        client_label.setStyleSheet("font-size: 18pt; color: black;")
        client_ver_layout.addWidget(client_label)
        
        client_widget = QWidget()
        client_widget.setLayout(client_ver_layout)
        self.setCentralWidget(client_widget)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
