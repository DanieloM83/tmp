from socket import *
import threading

HOST = "0.0.0.0"
PORT = 8080

server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

print(f"Server started on {HOST}:{PORT}")

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
        except:
            break

    clients.remove(client)
    client.close()

def accept_clients():
    while True:
        client, addr = server.accept()
        print(f"Connected: {addr}")
        clients.append(client)
        threading.Thread(
            target=handle_client,
            args=(client,),
            daemon=True
        ).start()

accept_clients()
