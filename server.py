import socket
import threading
from queue import Queue

# TODO:
# - implement parsing message into desired format: [sender]~[receiver]~[content]~[timestamp]~[sent]~[received]
# - implement datetime: 
#       when message sent: include time.time() 
#       when message received, perform datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
# - when users send "/message", it will only message desired client
# - a user can send "/group(A, B)" to form a group with clients A and B etc.
#       the user who initiated the group will be the admin, can add/remove members, edit group info and delete group 
# - implement message queue to save messages for offline users
# - implement file transfer
# - implement gui

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5678
SERVER_CONFIG = (HOST, PORT)
FORMAT = 'utf-8'
MSG_LENGTH = 2048
DISCONNECT_MSG = '/leave'

# Template for storing client data in dictionary
user = lambda username, socket, online : {"username": username, "client": socket, "online": online}

# list of clients connected to server
users = {} 

# active_clients = []

# Queue to store messages while user offline
message_queue = Queue()

# Creating server socket object
# AF_INET - IPv4 addresses will be used
# SOCK_STREAM - TCP packets will be used
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Attempts to create server at given HOST IP and PORT
try:
    server.bind(SERVER_CONFIG)
    print(f"[RUNNING] Server is running at {HOST} {PORT}")
except:
    print(f"[ERROR] Server unable to be created at host {HOST} and port {PORT}")

# Function to handle interaction of a client
# def client_handler(client):
    
#     connected = True
#     # Listens for client username
#     while True:
#         username = client.recv(2048).decode('utf-8')
         
#         if username != '':
#             active_clients.append((username, client))
#             break
#         else:
#             print("Client username is missing")
#     threading.Thread(target=message_listener, args=(client, username, )).start()
    


# # Function to listen for messages from a client
# def message_listener(client, username):

#     # Listens for client messages
#     while True:
#         message = client.recv(2048).decode('utf-8')

#         if message != '':
#             saved_msg = username + ': ' + message
#             broadcast(saved_msg)
#         else:
#             print(f"Message from client {username} is empty")


# # Function to send message to a single client
# def send_to_client(client, message):

#     client.sendall(message.encode())


# # Function to send messages to all active clients
# def broadcast(message):

#     for client in active_clients:
#         send_to_client(client[1], message)

# # Function to check if user exists in server
# def check_username(username):
#     for user in users:
#         if user["username"] == username:
#             return True
#     return False



def client_handler(client, address):
    print(f"[NEW CONNECTION] User {address} connected")
    connected = True
    
    username = client.recv(MSG_LENGTH).decode(FORMAT)
    # if username in users:
    #     users[username]["client"] = client
    #     users[username]["online"] = True
    # else:
    users[username] = user(username, client, True)
    # users.append((username, client))
        
    while connected:
        message = client.recv(MSG_LENGTH).decode(FORMAT)

        if message == DISCONNECT_MSG:
            connected = False

        print(f"{address}: {message}")
    
    client.close()
    users[username]["client"] = None
    users[username]["online"] = False



# Main function
def start():

    # # Creating server socket object
    # # AF_INET - IPv4 addresses will be used
    # # SOCK_STREAM - TCP packets will be used
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # print("[STARTING] Server is starting.....")

    # # Attempts to create server at given HOST IP and PORT
    # try:
    #     server.bind(SERVER_CONFIG)
    #     print(f"Server is running at {HOST} {PORT}")
    # except:
    #     print(f"Server unable to be created at host {HOST} and port {PORT}")
    
    print("[LISTENING] Server is listening on {HOST} {PORT}")
    # Listen for clients
    server.listen()
 
    while True:
        client, address = server.accept()
        print(f"Client {address[0]} {address[1]} successfully connected to server!")

        thread = threading.Thread(target=client_handler, args=(client, ))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


# if __name__ == "__main__":
#     main()

print("[STARTING] Server is starting.....")
start()
