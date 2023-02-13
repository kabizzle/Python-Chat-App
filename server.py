import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5678
SERVER_CONFIG = (HOST, PORT)

# LISTENER_LIMIT = 5

# list of clients connected to server
active_clients = []
usernames = []

# Function to handle interaction of a client
def client_handler(client):
    
    # Listens for client username
    while True:
        username = client.recv(2048).decode('utf-8')
         
        if username != '':
            active_clients.append((username, client))
            threading.Thread(target=message_listener, args=(client, username, )).start()
            break
        else:
            print("Client username is missing")
    


# Function to listen for messages from a client
def message_listener(client, username):

    # Listens for client messages
    while True:
        message = client.recv(2048).decode('utf-8')

        if message != '':
            saved_msg = username + ': ' + message
            broadcast(saved_msg)
        else:
            print(f"Message from client {username} is empty")


# Function to send message to a single client
def send_to_client(client, message):

    client.sendall(message.encode())


# Function to send messages to all active clients
def broadcast(message):

    for client in active_clients:
        send_to_client(client[1], message)


# Main function
def main():

    # Creating server socket object
    # AF_INET - IPv4 addresses will be used
    # SOCK_STREAM - TCP packets will be used
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("[STARTING] Server is starting.....")

    # Attempts to create server at given HOST IP and PORT
    try:
        server.bind(SERVER_CONFIG)
        print(f"Server is running at {HOST} {PORT}")
    except:
        print(f"Server unable to be created at host {HOST} and port {PORT}")
    
    # Listen for clients
    server.listen()
 
    while True:
        client, address = server.accept()
        print(f"Client {address[0]} {address[1]} successfully connected to server!")

        thread = threading.Thread(target=client_handler, args=(client, ))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
