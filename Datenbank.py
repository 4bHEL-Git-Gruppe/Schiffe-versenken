import sqlite3
import bcrypt
import secrets
import json

# Funktion zur Erstellung der Datenbank und Tabellen
def create_UserDB():
    """
    Erstellt die SQLite-Datenbank und Tabellen.

    Tabellen:
    - player:
        - userN (VARCHAR(20)): Primärschlüssel, Benutzername des Spielers.
        - pwd (TEXT): Gehashte Passwort des Spielers.
        - gamesP (INTEGER): Anzahl der gespielten Spiele des Spielers.
        - gamesW (INTEGER): Anzahl der gewonnenen Spiele des Spielers.
        - UserCode (TEXT): Einzigartiger Benutzer-Code, der beim Login generiert wird.

    - game:
        - id (INTEGER): Primärschlüssel, automatisch inkrementierte Spiel-ID.
        - P0 (TEXT): Benutzername von Spieler 0.
        - P1 (TEXT): Benutzername von Spieler 1.
        - status (TEXT): Status des Spiels, muss einer der folgenden Werte sein: 'Angehalten', 'Wird_gespielt', 'P1_won', 'P0_won'.
        - B0 (JSON): Brettzustand für Spieler 0.
        - B1 (JSON): Brettzustand für Spieler 1.
        - turn (BOOLEAN): Boolescher Wert, der anzeigt, wer an der Reihe ist.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            userN TEXT PRIMARY KEY,
            pwd TEXT NOT NULL,
            gamesP INTEGER DEFAULT 0,
            gamesW INTEGER DEFAULT 0,
            UserCode TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            P0 TEXT,
            P1 TEXT,
            status TEXT CHECK(status IN ('Angehalten', 'Wird_gespielt', 'P1_won', 'P0_won')),
            B0 JSON,
            B1 JSON,
            turn BOOLEAN,
            FOREIGN KEY (P0) REFERENCES player(userN),
            FOREIGN KEY (P1) REFERENCES player(userN)
        )
    ''')

    conn.commit()
    conn.close()

'''----------------------- Funktionen zum User speichern -----------------------'''

# Funktion zum Prüfen, ob ein Benutzer existiert
def checkUser(username: str) -> str:
    """
    Überprüft, ob ein Benutzer existiert.

    Parameter:
    username (str): Der Benutzername des Benutzers.

    Rückgabewert:
    str: Eine Meldung, die den Erfolg der Operation anzeigt oder darauf hinweist, dass der Benutzer nicht gefunden wurde.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM player WHERE userN = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return f"Benutzer '{username}' existiert."
    else:
        return False

# Funktion zum Hashen eines Passworts
def hashPassword(password: str) -> bytes:
    """
    Hasht das Passwort mit bcrypt.

    Parameter:
    password (str): Das Klartextpasswort, das gehasht werden soll.

    Rückgabewert:
    bytes: Das gehashte Passwort.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Funktion zur Überprüfung von Passwort
def checkPassword(hashedPassword: bytes, password: str) -> bool:
    """
    Überprüft das Passwort mit bcrypt.

    Parameter:
    hashedPassword (bytes): Das gehashte Passwort, das in der Datenbank gespeichert ist.
    password (str): Das Klartextpasswort, das überprüft werden soll.

    Rückgabewert:
    bool: True, wenn das Passwort korrekt ist, False ansonsten.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashedPassword)

# Funktion zur Registrierung einen neuen Benutzer
def SignUp(username: str, password: str) -> str:
    """
    Registriert einen neuen Benutzer, wenn der Benutzername noch nicht existiert.

    Parameter:
    username (str): Der gewünschte Benutzername des neuen Benutzers.
    password (str): Das Klartextpasswort des neuen Benutzers.

    Rückgabewert:
        str: Eine Meldung, die den Erfolg der Operation anzeigt oder darauf hinweist, dass der Benutzer bereits existiert.
    """
    hashedPassword = hashPassword(password)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT userN FROM player WHERE userN = ?', (username,))
    if cursor.fetchone():
        conn.close()
        return("User existiert bereits")
    else:
        cursor.execute('INSERT INTO player (userN, pwd) VALUES (?, ?)', (username, hashedPassword))
        conn.commit()
        conn.close()
        return("User erfolgreich registriert")

# Funktion zum Login eines Benutzers
def login(username: str, password: str) -> str:
    """
    Überprüft den Benutzer und generiert einen Benutzer-Code, wenn das Passwort korrekt ist.
    Gibt den Benutzer-Code zurück, wenn der Login erfolgreich ist.

    Parameter:
    username (str): Der Benutzername des Benutzers.
    password (str): Das Klartextpasswort des Benutzers.

    Rückgabewert:
    str: Der Benutzer-Code, wenn der Login erfolgreich ist, None ansonsten.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT pwd FROM player WHERE userN = ?', (username,))
    result = cursor.fetchone()
    if result:
        hashedPassword = result[0]
        if checkPassword(hashedPassword, password):
            print("Passwort ist korrekt")
            benutzerCode = secrets.token_hex(16)
            cursor.execute('UPDATE player SET UserCode = ? WHERE userN = ?', (benutzerCode, username))
            conn.commit()
            conn.close()
            return benutzerCode
        else:
            print("Passwort ist falsch")
    else:
        print("Username existiert nicht")

    conn.close()
    return None

# Funktion zum Hinzufügen eines Sieges
def addWin(username: str) -> str:
    """
    Erhöht die Anzahl der gewonnenen Spiele für den angegebenen Benutzer.

    Parameter:
    username (str): Der Benutzername des Benutzers.

    Rückgabewert:
    str: Eine Meldung, die den Erfolg der Operation anzeigt oder darauf hinweist, dass der Benutzer nicht gefunden wurde.
    """
    if checkUser(username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE player SET gamesW = gamesW + 1 WHERE userN = ?', (username,))
        conn.commit()
        conn.close()
        return (f"{username} hat Erfolgreich +1 Spiele gewonnen.")
    else:
        return "Benutzer nicht gefunden"

# Funktion zum Hinzufügen eines gespielten Spiels
def addGame(username: str) -> str:
    """
    Erhöht die Anzahl der gespielten Spiele für den angegebenen Benutzer.

    Parameter:
    username (str): Der Benutzername des Benutzers.

    Rückgabewert:
    str: Eine Meldung, die den Erfolg der Operation anzeigt oder darauf hinweist, dass der Benutzer nicht gefunden wurde.
    """
    if checkUser(username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE player SET gamesP = gamesP + 1 WHERE userN = ?', (username,))
        conn.commit()
        conn.close()
        return (f"{username} hat Erfolgreich +1 Spiele gespielt.")
    else:
        return "Benutzer nicht gefunden"

# Funktion zum Abrufen der Benutzerdaten
def getUserData(username: str) -> dict:
    """
    Ruft alle Daten für einen angegebenen Benutzer ab.

    Parameter:
    username (str): Der Benutzername des Benutzers.

    Rückgabewert:
    dict: Ein Wörterbuch mit den Benutzerdaten, falls der Benutzer existiert,
          andernfalls None.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM player WHERE userN = ?', (username,))
    userData = cursor.fetchone()
    conn.close()
    
    if userData:
        # Erstelle ein Wörterbuch mit den Benutzerdaten
        return {
            "Benutzername": userData[0],
            "Passwort": userData[1],
            "Gespielte Spiele": userData[2],
            "Gewonnene Spiele": userData[3],
            "Benutzer-Code": userData[4]
        }
    else:
        print("Benutzer nicht gefunden")
        return None

# Funktion zum Abrufen des Rankings
def getRanking() -> list:
    """
    Gibt Benutzer sortiert nach der Anzahl der gewonnenen und gespielten Spiele zurück.

    Rückgabewert:
    list: Eine Liste, die die Benutzer sortiert nach der Anzahl der gewonnenen Spiele
          in absteigender Reihenfolge und der Anzahl der gespielten Spiele in aufsteigender Reihenfolge enthält.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT userN, gamesP, gamesW FROM player ORDER BY gamesW DESC, gamesP ASC')
    ranking = cursor.fetchall()
    conn.close()
    return ranking

# Funktion zum Abrufen aller Benutzerdaten
def getAllUser() -> list:
    """
    Gibt alle Benutzerdaten zurück.

    Rückgabewert:
    list: Liste aller Benutzer.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM player')
    allUsers = cursor.fetchall()
    conn.close()
    return allUsers

# Funktion zum Logout eines Benutzers
def logout(username: str) -> str:
    """
    Löscht den Benutzer-Code eines Benutzers.

    Parameter:
    username (str): Der Benutzername des Benutzers.

    Rückgabewert:
    str: Eine Meldung, die den Erfolg der Operation anzeigt oder darauf hinweist, dass der Benutzer nicht gefunden wurde.
    """
    if checkUser(username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE player SET UserCode = NULL WHERE userN = ?', (username,))
        conn.commit()
        conn.close()
        return f"Benutzer '{username}' erfolgreich abgemeldet."
    else:
        return "Benutzer nicht gefunden"

# Funktion zum Löschen eines Benutzers
def delete(username: str) -> str:
    """
    Löscht einen Benutzer aus der Datenbank.

    Parameter:
    username (str): Der Benutzername des Benutzers.

    Rückgabewert:
    str: Eine Meldung, die den Erfolg der Operation anzeigt oder darauf hinweist, dass der Benutzer nicht gefunden wurde.
    """
    if checkUser(username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM player WHERE userN = ?', (username,))
        conn.commit()
        conn.close()
        return f"Benutzer '{username}' erfolgreich gelöscht."
    else:
        return "Benutzer nicht gefunden"

# Funktion zum Aktualisieren der Benutzerdaten
def update(username: str, gamesPlayed: int, gamesWon: int) -> str:
    """
    Aktualisiert die Anzahl der gespielten und gewonnenen Spiele eines Benutzers.

    Parameter:
    username (str): Der Benutzername des Benutzers.
    gamesPlayed (int): Die Anzahl der gespielten Spiele.
    gamesWon (int): Die Anzahl der gewonnenen Spiele.

    Rückgabewert:
    str: Eine Meldung, die den Erfolg der Operation anzeigt oder darauf hinweist, dass der Benutzer nicht gefunden wurde.
    """
    if checkUser(username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE player SET gamesP = ?, gamesW = ? WHERE userN = ?', (gamesPlayed, gamesWon, username))
        conn.commit()
        conn.close()
        return f"Spiele-Daten von Benutzer '{username}' erfolgreich aktualisiert."
    else:
        return "Benutzer nicht gefunden"

# Funktion zum Aktualisieren des Benutzerpassworts
def updatePassword(username: str, password: str) -> str:
    """
    Aktualisiert das Passwort eines Benutzers.

    Parameter:
    username (str): Der Benutzername des Benutzers.
    password (str): Das neue Klartextpasswort des Benutzers.

    Rückgabewert:
    str: Eine Meldung, die den Erfolg der Operation anzeigt oder darauf hinweist, dass der Benutzer nicht gefunden wurde.
    """
    if checkUser(username):
        hashedPassword = hashPassword(password)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE player SET pwd = ? WHERE userN = ?', (hashedPassword, username))
        conn.commit()
        conn.close()
        return f"Passwort von Benutzer '{username}' erfolgreich aktualisiert."
    else:
        return "Benutzer nicht gefunden"

# Funktion zum Abrufen des Benutzer-Codes
def getBenutzerCode(username: str) -> str:
    """
    Gibt den Benutzer-Code eines Benutzers zurück.

    Parameter:
    username (str): Der Benutzername des Benutzers.

    Rückgabewert:
    str: Der Benutzer-Code des Benutzers oder eine Meldung, dass der Benutzer nicht gefunden wurde.
    """
    if checkUser(username):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT UserCode FROM player WHERE userN = ?', (username,))
        benutzerCode = cursor.fetchone()
        conn.close()
        return benutzerCode[0] if benutzerCode else "Benutzercode nicht gefunden"
    else:
        return "Benutzer nicht gefunden"
  
# Funktion zur Überprüfung des Benutzer-Codes
def benutzerCodeCheck(benutzerCode: str) -> str:
    """
    Überprüft, ob ein Benutzer-Code gültig ist und gibt den zugehörigen Benutzernamen zurück.

    Parameter:
    benutzerCode (str): Der zu überprüfende Benutzer-Code.

    Rückgabewert:
    str: Der Benutzername des Benutzers, wenn der Code gültig ist, andernfalls eine Meldung, dass der Benutzer nicht gefunden wurde.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT userN FROM player WHERE UserCode = ?', (benutzerCode,))
    username = cursor.fetchone()
    conn.close()
    return username[0] if username else "Benutzer nicht gefunden"

'''----------------------- Funktionen zum Spiel speichern -----------------------'''

# Funktion zum Speichern eines Spiels
def saveGame(P0: str, P1: str, b0: str, b1: str, turn: bool) -> str:
    """
    Speichert ein Spiel mit den angegebenen Spielern, Brettern und Zügen.
    Wenn ein Spiel mit den gleichen Spielern bereits existiert, wird es aktualisiert.

    Parameter:
    P0 (str): Benutzername von Spieler 0.
    P1 (str): Benutzername von Spieler 1.
    b0 (str): Brettzustand von Spieler 0.
    b1 (str): Brettzustand von Spieler 1.
    turn (bool): Boolescher Wert, der anzeigt, wer an der Reihe ist.
    
    Rückgabewert:
    str: Eine Meldung, die den Erfolg der Operation anzeigt.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # JSON in einen String umwandeln
    b0_json = json.dumps(b0)
    b1_json = json.dumps(b1)

    # Überprüfen, ob ein Spiel mit den gleichen Spielern bereits existiert
    cursor.execute('SELECT id FROM game WHERE P0 = ? AND P1 = ?', (P0, P1))
    game = cursor.fetchone()

    # Spielstatus
    status = "Angehalten"

    if game:
        # Aktualisiere das bestehende Spiel
        cursor.execute('''
            UPDATE game 
            SET B0 = ?, B1 = ?, turn = ?
            WHERE id = ?
        ''', (b0_json, b1_json, turn, game[0]))
        conn.commit()
        conn.close()

        return "Das Spiel wurde aktualisiert."
    else:
        # Füge ein neues Spiel in die 'game'-Tabelle ein
        cursor.execute('''
            INSERT INTO game (P0, P1, status, B0, B1, turn)
            VALUES (?, ?, ?, ?, ?, ?) 
        ''', (P0, P1, status, b0, b1, turn))
        conn.commit()
        conn.close()
        return "Ein neues Spiel wurde hinzugefügt."

# Funktion zum Abrufen aller Spieldaten
def getAllGame() -> list:
    """
    Gibt alle Spieldaten zurück.

    Rückgabewert:
    list: Liste aller Spiele.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM game')
    allgames = cursor.fetchall()
    conn.close()
    return allgames

# Funktion zum Abrufen der Spieldaten
def getGameData(P0: str, P1: str) -> dict:
    """
    Gibt die Brettdaten eines bestimmten Spiels zurück.
    Findet die korrekten Daten unabhängig von der Reihenfolge der Spieler.

    Parameter:
    P0 (str): Benutzername von Spieler 0.
    P1 (str): Benutzername von Spieler 1.

    Rückgabewert:
    dict: Spieldaten einschließlich ID, Spielern, Status, Brettern und Zug.
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Suche nach dem Spiel unabhängig von der Reihenfolge der Spieler
    cursor.execute('''
        SELECT * FROM game
        WHERE (P0 = ? AND P1 = ?) OR (P0 = ? AND P1 = ?)
    ''', (P0, P1, P1, P0))
    
    gameData = cursor.fetchone()
    conn.close()
    
    if gameData:
        return {
            "id": gameData[0],
            "P0": gameData[1],
            "P1": gameData[2],
            "status": gameData[3],
            "B0": gameData[4],
            "B1": gameData[5],
            "turn": gameData[6]
        }
    else:
        print("Kein Spiel gefunden")
        return None

# Funktion zum Aktualisieren des Spielstatus
def updateGameStatus(P0: str, P1: str, status: str) -> str:
    """
    Aktualisiert den Status eines Spiels mit den angegebenen Spielern.

    Parameter:
    P0 (str): Benutzername von Spieler 0.
    P1 (str): Benutzername von Spieler 1.
    status (str): Neuer Status des Spiels, muss einer der folgenden Werte sein: 'Angehalten', 'Wird_gespielt', 'P1_won', 'P0_won'.

    Rückgabewert:
    str: Eine Meldung, die den Erfolg oder Misserfolg der Operation anzeigt.
    """
    gültige_status = ['Angehalten', 'Wird_gespielt', 'P1_won', 'P0_won']
    if status not in gültige_status:
        return f"Ungültiger Status. Status muss einer der folgenden sein: " + ", ".join(gültige_status)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Suchen nach dem Spiel unabhängig von der Reihenfolge der Spieler
    cursor.execute('''
        SELECT id FROM game
        WHERE (P0 = ? AND P1 = ?) OR (P0 = ? AND P1 = ?)
    ''', (P0, P1, P1, P0))
    
    spiel = cursor.fetchone()

    if spiel:
        cursor.execute('''
            UPDATE game 
            SET status = ? 
            WHERE id = ?
        ''', (status, spiel[0]))
        conn.commit()
        conn.close()
        return "Spielstatus erfolgreich aktualisiert"
    else:
        return "Kein Spiel zwischen diesen Spielern gefunden"

def getMyGame(Player: str) -> dict:
    """
    Gibt eine Liste aller Spiele zurück, an denen der Spieler P teilnimmt.

    Parameter:
    P (str): Benutzername von Spieler.

    Rückgabewert:
    dict: Spieldaten einschließlich ID, Spielern, Status, Brettern und Zug. 
    """
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Suche nach dem Spiel unabhängig von der Reihenfolge der Spieler
    cursor.execute('''
        SELECT * FROM game
        WHERE (P0 = ?) OR (P1 = ?)
    ''', (Player, Player))
    
    gameData = cursor.fetchone()
    conn.close()
    
    if gameData:
        return {
            "id": gameData[0],
            "P0": gameData[1],
            "P1": gameData[2],
            "status": gameData[3],
            "B0": gameData[4],
            "B1": gameData[5],
            "turn": gameData[6]
        }

# Beispiel
'''if __name__ == "__main__":
    bourd = {
        "schif 1": {"size": [1,5] , "position": ["x","y"], "destroyedParts": ["x,y", "x,y", "x,y"]},
        "schif 2": {"size": [1,4] , "position": ["x","y"], "destroyedParts": ["x,y", "x,y", "x,y"]},
        "schif 3": {"size": [1,3] , "position": ["x","y"], "destroyedParts": ["x,y", "x,y", "x,y"]},
        "schif 4": {"size": [1,3] , "position": ["x","y"], "destroyedParts": ["x,y", "x,y", "x,y"]},
        "schif 5": {"size": [1,2] , "position": ["x","y"], "destroyedParts": ["x,y", "x,y", "x,y"]},
        "miss" : ["x,y", "x,y", "x,y"]
        }
    create_UserDB()
    SignUp("testuser0", "password")
    SignUp("testuser1", "password")
    print(addWin("testuser1"))

    login("testuser0", "password")
    login("testuser1", "password")   

    saveGame("testuser0", "testuser1", bourd, bourd, 0)

    print(updateGameStatus("testuser1", "testuser0", "Wird_gespielt"))

    print(getMyGame("testuser0"))'''