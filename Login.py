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
        
        # Hauptlayout
        main_layout = QGridLayout()
        vert_layout = QVBoxLayout()
        hort1_layout = QHBoxLayout()
        hort2_layout = QHBoxLayout()
        hort3_layout = QHBoxLayout()
        horb_layout = QHBoxLayout()

        #Top

        # Hintergrund Label
        hintergrund_top = QLabel("")
        hintergrund_top.setStyleSheet("background-color : rgba(40,40,40, 70); "
                                      "border : 2px solid grey;"
                                      "border-radius: 10%;")
        hintergrund_top.setFixedSize(530, 115)
        
        #Vertical 1
        #Anweisungen 
        anweisung_label = QLabel("Gib hier deine Daten ein: ")
        anweisung_label.setStyleSheet("QLabel { color : rgb(255,255,255); "
                                    "font-size : 18pt;"
                                    "border : 2px solid rgba(255,255,255,80);"
                                    "border-radius: 10%;"
                                    "}")
        anweisung_label.setFixedSize(280, 35)

        hort1_layout.addWidget(anweisung_label)

        vert_layout.addLayout(hort1_layout)

        #Vertical 2
        #Username Label
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


        #Vertical 3
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


        #Bottom

        hintergrund_bottom = QLabel("")
        hintergrund_bottom.setStyleSheet("background-color : rgba(40,40,40, 70); "
                           "border : 2px solid grey;"
                           "border-radius: 10%;")
        hintergrund_bottom.setFixedSize(530, 110)

        welcome = QLabel("Ey Kamerad, willst du dich ")
        welcome.setStyleSheet("font-size : 14pt")
        welcome.setFixedSize(220, 35)
        horb_layout.addWidget(welcome)

        signup = QPushButton("Einloggen")
        signup.setStyleSheet("font-size : 14pt")
        signup.setFixedSize(110, 35)
        horb_layout.addWidget(signup)

        oder = QLabel("oder")
        oder.setStyleSheet("font-size : 14pt")
        oder.setFixedSize(40, 35)
        horb_layout.addWidget(oder)

        register = QPushButton("Registrieren")
        register.setStyleSheet("font-size : 14pt")
        register.setFixedSize(120, 35)
        horb_layout.addWidget(register)        
        

        # Set spacing and margins to reduce distance between widgets
        hort1_layout.setSpacing(0)  # Adjust this value as needed
        hort1_layout.setContentsMargins(40, 3, 0, 0)

        hort2_layout.setSpacing(5)  # Adjust this value as needed
        hort2_layout.setContentsMargins(180, 0, 150, 0)

        hort3_layout.setSpacing(5)  # Adjust this value as needed
        hort3_layout.setContentsMargins(180, 0, 150, 0)

        vert_layout.setSpacing(5)  # Adjust this value as needed
        vert_layout.setContentsMargins(0, 0, 0, 0)

        horb_layout.setSpacing(5)  
        horb_layout.setContentsMargins(10, 0, 0, 37)

        # Hinzufügen der Widgets zum Hauptlayout
        main_layout.addWidget(hintergrund_top, 0, 0, Qt.AlignmentFlag.AlignTop)
        main_layout.addLayout(vert_layout, 0, 0, Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(hintergrund_bottom, 2, 0, Qt.AlignmentFlag.AlignBottom)
        main_layout.addLayout(horb_layout, 2, 0, Qt.AlignmentFlag.AlignBottom)

        

        # Stretch-Faktor hinzufügen, um Platz nach unten zu drücken
        main_layout.setRowStretch(2, 1)
        main_layout.setContentsMargins(0,10,1,10)

        # Set central widget with layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Apply stylesheet to main window for background image
        self.setStyleSheet("""
            QMainWindow {
                background-image: url(login_bild2.jpg);
                background-position: center;
                background-repeat: no-repeat;
            }
        """)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()





"""def hintergrundbild(self):
        self.bild  = QPixmap("login_bild2.jpg")
        self.hintergrund = QLabel()
        self.hintergrund.setPixmap(self.bild)
        self.hintergrund.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.hintergrund, 0, 0, 3, 3)"""