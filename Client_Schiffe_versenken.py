import socket    
import pickle

# Socket für die Verbindung zum Server erstellen
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('127.0.0.1', 10000))
Player = server.recv(10).decode()
print(f"Erfolgreich verbunden, Sie sind {Player}")

