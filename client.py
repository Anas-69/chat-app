import socket
import threading
import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65535
BUFFER_SIZE = 1024

def send_message(client):
    while True:
        try:
            message = input("Enter your message: ")
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
            # Handle error or reconnection logic here if needed

def receive_message(client):
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode('utf-8')
            print(message)
        except ConnectionResetError:
            print("Connection to the server closed.")
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to the server.")
        
        send_thread = threading.Thread(target=send_message, args=(client,))
        receive_thread = threading.Thread(target=receive_message, args=(client,))
        
        send_thread.start()
        receive_thread.start()
        
        send_thread.join()
        receive_thread.join()
        
        break  # If connection and threads started successfully, exit the reconnect loop
    
    except Exception as e:
        print(f"Connection error: {e}")
        print("Attempting to reconnect in 5 seconds...")
        time.sleep(5)  # Wait for 5 seconds before the next reconnection attempt