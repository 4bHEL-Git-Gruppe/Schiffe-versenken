import socket
import pickle

# Server initialisieren und auf Verbindungen warten
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 10000))
server.listen(2)

print("Auf Spieler Warten...")

Spieler_liste = []
# Zwei Spieler akzeptieren und ihre Sockets speichern
for _ in range(1):
    client, addr = server.accept()
    Spieler_liste.append((client, addr))
    print(f"Verbunden mit {addr}")

Spieler_liste[0][0].send("Player1".encode())
#Spieler_liste[1][0].send("Player2".encode())

