import socket
import select

class CommunicationServer:
    #Konstruktro
    def __init__(self,host, port):
        self.host = host
        self.port = port
        self.server = None
        self.clients = []

    #Server starten
    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        print("Server started")
        self.server.listen(2)

    #Auf Spieler warten mit Anzahl kann mit anz bestimmt werden
    def wait_for_players(self, anz):
        print(f"Waiting for {anz} players...")
        while len(self.clients) < anz:
            client, addr = self.server.accept()
            self.clients.append(client)
            print(f"Connected with player {len(self.clients)} at address {addr}")
        #print("Liste mit Clients: ",self.clients)
    
    #einfache SendData Methode für Strings
    def send_data(self,data,player):
        self.clients[player].send(data.encode())

    #Receive Data Methode um egal welche Spieler Daten sendet diese zu empfangen
    def receive_data(self):
        readable, _, _ = select.select(self.clients, [], [])
        for sock in readable:
            data = sock.recv(1024).decode()
            if data:
                return data, sock.getpeername()
        return None, None

#Mainprogramm für Testzecke
if __name__ == "__main__":
    server = CommunicationServer("127.0.0.1",61112)
    server.start_server()
    server.wait_for_players(2)
    server.send_data("Player 1", 0)
    server.send_data("Player 2", 1)

    while True:
        data, addr = server.receive_data()
        if data:
            print(f"Received from {addr}: {data}")
