import socket

class CommunicationServer:
    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.server = None

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        print("Server started")
        self.server.listen(2)

    def wait_for_players(self,anz):
        self.server.listen(anz)
        print("Waiting for Players...")
        self.players = []
        for i in range(anz):
            client, addr = self.server.accept()
            self.players.append((client, addr))
            print(f"Verbunden mit Spieler {i + 1} bei Adresse {addr}")
    
    def SendData(self,data,player):
        if player==0:
            self.players[0][0].send(data.encode())
        else:
            self.players[1][0].send(data.encode())

    def ReciveData(self):
        data = self.server.recv(1024).decode()
        return data


