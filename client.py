import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5678
SERVER_CONFIG = (HOST, PORT)
FORMAT = 'utf-8'
MSG_LENGTH = 2048
DISCONNECT_MSG = '/leave'

# Function to listen for messages from server
def listen_to_server(client):

    while True:
        message = client.recv(MSG_LENGTH).decode(FORMAT)

        if message != '':
            # username = message.split(":")[0]
            # content = message.split(":")[1]
            print('\n' + message)
        else:
            print("Message received from client is empty")


# Function to send communicate client info with server
def initialise_on_server(client):

    username = input("Please enter your username: ")

    while username == '':
        print("Username cannot be empty.")
        username = input("Please enter your username: ")

    # if username != '':
    #     client.sendall(username.encode())
    # else:
        # print("Username cannot be empty.")
    
    client.sendall(username.encode())
         
    threading.Thread(target=listen_to_server, args=(client, )).start()
    send_message_to_server(client)


# Function to send message to server
def send_message_to_server(client):
    while True:
        message = input()    

        if message != '':
            client.sendall(message.encode())


# Main function
def start():

    # Creating client socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to server
    try:
        client.connect(SERVER_CONFIG)
        print(f"Client successfully connected to server {HOST} {PORT}")
    except:
        print(f"Client unable to connect to server {HOST} {PORT}")

    initialise_on_server(client)

# if __name__ == "__main__":
#     main()

start()