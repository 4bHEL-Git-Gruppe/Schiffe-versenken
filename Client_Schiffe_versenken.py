import socket    
import time

class CommunicationClient:
    #Konstruktor
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.client = None
    #Verbindung aufbauen
    def start_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        print(f"Client auf {self.host} verbunden")
    #einfache sendData Methode für String
    def sendData(self,data):
        self.client.send(data.encode())
    #einfache ReceiveData Methode für Strings
    def receivData(self):
        data = self.client.recv(1024).decode()
        return data
    
    #eigens für Taha Methode für Login und weitere Metadaten
    def send_command(self, command, *args):
        message = ','.join([command] + list(args))
        print(message)
        self.client.send(message.encode())
        #response = self.client.recv(1024).decode()
        #return response

    #Methode um die Schiffe am Anfang vom Spiel zu platzieren
    def place_ships(self,ship_list,name):
        ship_string = self.formatiere_liste(ship_list,name)
        self.sendData(ship_string)

    #Methode um die Schiffe abschießen zu können
    def fire(self,pos,name):
        pos_string = self.formatiere_liste([pos],name)
        self.sendData(pos_string)

    #um intern von einer Liste auf einen String zu konvertieren
    def formatiere_liste(self,pos,name):
        # Konvertiere jede Koordinate in einen String mit Komma getrennt
        koordinaten_str = [f"{x},{y}" for x, y in pos]
        # Verbinde die Koordinaten mit ';'
        koordinaten_liste = ";".join(koordinaten_str)
        # Füge den Namen am Anfang des Strings mit ':' getrennt hinzu
        ergebnis_str = f"{name}:{koordinaten_liste}"
        return ergebnis_str
    
#Mainprogramm für Testzwecke
if __name__ == "__main__":
    client = CommunicationClient("127.0.0.1",61112)
    pos = [[0,0],[0,1],[1,0]]
    client.start_client()
    spielername = client.receivData()
    print(spielername)
    username = input("Username eingeben: ")
    password = input("Passwort eingeben: ")
    client.send_command("SignUp",username,password)
    time.sleep(1)
    client.place_ships(pos,spielername)