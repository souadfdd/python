#!/usr/bin/env python3
#from socket import AF_INET, socket, SOCK_STREAM
import socket
from threading import Thread


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s est connecte." % client_address)
        client.send(bytes("Entrez votre Prenom et cliquez ENTRER!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # client = socket
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bienvenue %s! si vous voulez quitter, saisir --quitter--.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s est en ligne!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("--quitter--", "utf8"):
            broadcast(msg, "+ "+name+": ")
        else:
            client.send(bytes("--quitter--", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s a quitte le chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix = le nom
    """envoyer le message a toutes les personnes connectees"""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}


HOST = ''
#HOST = socket.gethostbyname(socket.gethostname())
print("Host: ", HOST)
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Attente de connexion...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
