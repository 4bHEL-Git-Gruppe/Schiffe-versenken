# Schiffe-versenken

                                 ###CommunicationServer###
CommunicationServer ist eine Python-Klasse, die es ermöglicht, einen einfachen Server zu 
erstellen, der mit mehreren Clients über das Netzwerk kommunizieren kann. Die Klasse verwendet 
die socket-Bibliothek, um Verbindungen herzustellen und Daten zu senden und zu empfangen.

##Methoden

__init__(self, host, port)
Konstruktor zum Initialisieren des Servers.
host: Die IP-Adresse des Servers.
port: Der Port, an dem der Server lauscht.

start_server(self)
Startet den Server und bindet ihn an die angegebene IP-Adresse und den Port.

wait_for_players(self, anz)
Wartet auf die angegebene Anzahl von Spielern und akzeptiert deren Verbindungen.
anz: Die Anzahl der Spieler, auf die gewartet werden soll.

SendData(self, data, player)
Sendet Daten an den angegebenen Spieler.
data: Die zu sendenden Daten.
player: Der Index des Spielers (0 für Spieler 1, 1 für Spieler 2).

ReciveData(self)
Empfängt Daten vom Server.
Rückgabewert: Die empfangenen Daten.



                                    ###CommunicationClient###
CommunicationClient ist eine Python-Klasse, die es ermöglicht, einen einfachen Client zu 
erstellen, der mit einem Server über das Netzwerk kommunizieren kann. Die Klasse verwendet 
die socket-Bibliothek, um Verbindungen herzustellen und Daten zu senden und zu empfangen.

##Methoden
__init__(self, host, port)
Konstruktor zum Initialisieren des Clients.
host: Die IP-Adresse des Servers.
port: Der Port, an dem der Server lauscht.

start_client(self)
Startet den Client und stellt eine Verbindung zum Server her.

sendData(self, data)
Sendet Daten an den Server.
data: Die zu sendenden Daten.

recivData(self)
Empfängt Daten vom Server.
Rückgabewert: Die empfangenen Daten.