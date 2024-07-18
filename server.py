import socket
import threading

SERVER_HOST = '127.0.0.1'  # Listen on localhost
SERVER_PORT = 65535  # Use a specific port for your server
BUFFER_SIZE = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(5)  # Listen for incoming connections (max 5)

connected_clients = []

def handle_client(client_socket, client_address):
    connected_clients.append(client_socket)
    print(f"New connection from {client_address}")

    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')

            for client in connected_clients:
                if client != client_socket:
                    client.send(message.encode('utf-8'))

        except ConnectionResetError:
            print(f"Connection with {client_address} closed.")
            connected_clients.remove(client_socket)
            break

while True:
    client_socket, client_address = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()