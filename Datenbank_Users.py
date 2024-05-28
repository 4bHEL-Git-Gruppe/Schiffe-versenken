import sqlite3
import bcrypt
import secrets

def create_UserDB():
    """Erstellt die SQLite-Datenbank und die Tabelle"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        hashedPassword TEXT NOT NULL,
                        gamesPlayed INTEGER DEFAULT 0,
                        gamesWon INTEGER DEFAULT 0,
                        benutzerCode TEXT
                      )''')
    conn.commit()
    conn.close()

def hashPassword(password):
    """Hashing des Passworts mit bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def checkPassword(hashedPassword, password):
    """Überprüft das Passwort mit bcrypt"""
    return bcrypt.checkpw(password.encode(), hashedPassword)

def SignUp(username, password):
    """Fügt einen neuen Benutzer hinzu, wenn der Benutzername noch nicht existiert"""
    hashedPassword = hashPassword(password)
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return("User existiert bereits")
    else:
        cursor.execute("INSERT INTO users (username, hashedPassword) VALUES (?, ?)", (username, hashedPassword))
        conn.commit()
        return("User erfolgreich hinzugefügt")
    conn.close()

def login(username, password):
    """
    Überprüft den Benutzer und generiert einen Benutzercode bei korrektem Passwort.
    Gibt den Benutzercode zurück, wenn der Login erfolgreich ist.
    """
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT hashedPassword FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        if checkPassword(result[0], password):
            benutzerCode = secrets.token_hex(16)
            cursor.execute("UPDATE users SET benutzerCode = ? WHERE username = ?", (benutzerCode, username))
            conn.commit()
            print("Passwort ist korrekt")
            return benutzerCode
        else:
            print("Passwort ist falsch")
    else:
        print("User existiert nicht")
    conn.close()
    return None

def addWin(username):
    """Erhöht die Anzahl der gewonnenen Spiele für den angegebenen Benutzer"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET gamesWon = gamesWon + 1 WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def addgame(username):
    """Erhöht die Anzahl der gespielten Spiele für den angegebenen Benutzer"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET gamesPlayed = gamesPlayed + 1 WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def getUserData(username):
    """Ruft alle Daten eines Benutzers ab und gibt sie zurück"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

def getRanking():
    """Gibt die Benutzer sortiert nach Anzahl der gewonnenen und gespielten Spiele zurück"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY gamesWon DESC, gamesPlayed DESC")
    ranking = cursor.fetchall()
    conn.close()
    return ranking

def getAll():
    """Gibt alle Benutzerdaten zurück"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    conn.close()
    return all_users

def logout(username):
    """Löscht den Benutzercode eines Benutzers"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET benutzerCode = NULL WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def delete(username):
    """Löscht einen Benutzer aus der Datenbank"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def update(username, gamesPlayed, gamesWon):
    """Aktualisiert die Spiele-Daten (gamesPlayed und gamesWon) eines Benutzers"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET gamesPlayed = ?, gamesWon = ? WHERE username = ?", (gamesPlayed, gamesWon, username))
    conn.commit()
    conn.close()

def updatePassword(username, password):
    """Aktualisiert das Passwort eines Benutzers"""
    hashedPassword = hashPassword(password)
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET hashedPassword = ? WHERE username = ?", (hashedPassword, username))
    conn.commit()
    conn.close()

def updateUsername(username, newUsername):
    """Aktualisiert den Benutzernamen eines Benutzers"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ? WHERE username = ?", (newUsername, username))
    conn.commit()
    conn.close()

#new 

def getBenutzerCode(username):
    """Gibt den Benutzercode eines Benutzers zurück"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT benutzerCode FROM users WHERE username = ?", (username,))
    benutzerCode = cursor.fetchone()[0]
    conn.close()
    return benutzerCode

def benutzerCheck(benutzerCode):
    """Überprüft, ob ein Benutzercode gültig ist und welchem user es gehort"""
    conn = sqlite3.connect('userdb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE benutzerCode = ?", (benutzerCode,))
    username = cursor.fetchone()[0]
    conn.close()
    return username

'''
# Beispiel
if __name__ == "__main__":
    create_UserDB()

    status1 = SignUp("user1", "password1")
    status2 = SignUp("user2", "password1")
    print(status1)
    print(status2)

    benutzerCode = login("user1", "password1")
    if benutzerCode:
        print("Benutzercode:", benutzerCode)
          
    benutzerCodeCheck = getBenutzerCode("user1")
    print("Benutzercode:", benutzerCodeCheck)

    addWin("user1")
    addgame("user1")

    currentUser = benutzerCheck(benutzerCode)
    print("currentUser:", currentUser)
    print(getAll())
'''