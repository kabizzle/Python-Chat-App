import socket
import threading

HOST = '192.168.31.168'
PORT = 5678
SERVER_CONFIG = (HOST, PORT) 
NAME_CHOSEN = False
MSG_VALID = False

# Function to listen for messages from server
def listen_to_server(client):

    while True:
        message = client.recv(2048).decode('utf-8')

        if message != '':
            # username = message.split(":")[0]
            # content = message.split(":")[1]
            print(message)
        else:
            print("Message received from client is empty")


# Function to send communicate client info with server
def initialise_on_server(client):

    username = input("Please enter your username: ")

    if username != '':
        client.sendall(username.encode())
    else:
        print("Username cannot be empty.")
        exit(0)
         
    threading.Thread(target=listen_to_server, args=(client, )).start()
    send_message_to_server(client)


# Function to send message to server
def send_message_to_server(client):
    while True:
        message = input("Message: ")    

        if message != '':
            client.sendall(message.encode())
        else:
            print("Message cannot be empty.")
            exit(0)


# Main function
def main():

    # Creating client socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to server
    try:
        client.connect(SERVER_CONFIG)
        print(f"Client successfully connected to server {HOST} {PORT}")
    except:
        print(f"Client unable to connect to server {HOST} {PORT}")

    initialise_on_server(client)

if __name__ == "__main__":
    main()
