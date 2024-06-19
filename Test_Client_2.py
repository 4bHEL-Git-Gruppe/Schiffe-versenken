from Client_Schiffe_versenken import CommunicationClient

client2 = CommunicationClient("127.0.0.1",61112)
client2.start_client()
print(client2.receivData())
username = input("Username eingeben: ")
password = input("Passwort eingeben: ")
client2.send_command("SignUp",username,password)
client2.fire([0,3],"420")