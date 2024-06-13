import socket    

class CommunicationClient:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.client = None
    def start_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        print(f"Client auf {self.host} verbunden")

    def sendData(self,data):
        self.client.send(data.encode())

    def recivData(self):
        data = self.client.recv(1024).decode()
        return data


