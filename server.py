import socket
import threading
from queue import Queue
from datetime import datetime

# TODO:
# - identify direct vs groupchat messages
#       copy string format for broadcast message and add 'from [user]' or 'from [group]'
# - the group chat admin can add/remove members, edit group info and delete group 
# - check if gp members in server
# - handle leaving server in client - exit to terminal
# - implement message queue to save messages for offline users
# - implement choosing whether to use IPv4 or IPv6
# - implement file transfer
# - implement gui
# ? implement parsing message into desired format: [sender]~[receiver]~[content]~[timestamp]~[sent]~[received]

# DONE:
# - when users send dm command, it will only message desired client
# - a user can send group chat command to form a group with clients A and B etc.
# - implement datetime: 
#       when message sent: include time.time() 
#       when message received, perform datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
# - let users know when added to a group chat
# - make creating group chat a command in group mode rather than default
# - users can send messages to group even if they didnt create it

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5678
SERVER_CONFIG = (HOST, PORT)
FORMAT = 'utf-8'
MSG_LENGTH = 2048
DIRECT_MSG = '/direct'
GROUP_MSG = '/group'
DISCONNECT_MSG = '/leave'

# Template for storing client data in dictionary
user = lambda username, socket, online : {"username": username, "client": socket, "online": online}

# list of clients connected to server
users = {} 

# list of group chats in server
groups = {}

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


# Function to send message to a single client
def send_to_client(client, message):
    client.sendall(message.encode(FORMAT))


# Function to send messages to all active clients
def broadcast(message):
    for client in users.keys():
        send_to_client(users[client]["client"], message)

def direct(username, message):
    if username in users.keys():
        if users[username]["online"]:
            send_to_client(users[username]["client"], message)
        else:
            message_queue.put(message)

def group(group_name, message):
    group_users = groups[group_name]["users"]
    for member in group_users:
        send_to_client(users[member]["client"], message)


# # Function to check if user exists in server
# def check_username(username):
#     for user in users:
#         if user["username"] == username:
#             return True
#     return False

def create_group(group_name, usernames, admin):
    groups[group_name] = {"users": usernames, "admin": admin}

def check_user_groups(username):
    group_list = []
    for group in groups.keys():
        if username in groups[group]["users"]:
            group_list.append(group)
    
    return group_list


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
        time = datetime.now()

        if message == DISCONNECT_MSG:
            send_to_client(client, "/leave")
            connected = False

        elif message == DIRECT_MSG:
            send_to_client(client, "You have entered direct message mode!\nSend direct messages to a user in format '[username]~[message]'\nSend 'exit' to return to general chat")
            direct_mode = True
            while direct_mode:
                new_msg = client.recv(MSG_LENGTH).decode(FORMAT)
                if '~' in new_msg:
                    parsed_msg = new_msg.split('~')
                    direct(parsed_msg[0], parsed_msg[1])
                elif new_msg == 'exit':
                    direct_mode = False
                else:
                    send_to_client(client, "Incorrect format, direct message not sent")
        
        elif message == GROUP_MSG:
            send_to_client(client, "You have entered group chat mode!\nSend 'exit' to return to general chat")
            user_groups = check_user_groups(username)

            send_to_client(client, "Would you like to create a new group? y/n")
            resp = client.recv(MSG_LENGTH).decode(FORMAT)
            if resp == "y":
                send_to_client(client, "Enter a name for your group chat:") 
                group_name = client.recv(MSG_LENGTH).decode(FORMAT)
                send_to_client(client, "Add users to group chat using format '[username]~[username]~...'")
                group_users = client.recv(MSG_LENGTH).decode(FORMAT)
                parsed_group_users = group_users.split('~')
                parsed_group_users.append(username)
                # check if user is part of group before creating
                create_group(group_name, parsed_group_users, username)
                # groups[group_name] = {"users": parsed_group_users, "admin": username}
                group(group_name, f"You have been added to the group chat{group_name}!")

            send_to_client(client, f"You are a member of the following group chats: {user_groups}\nSend a message of the form '[group name]~[message]' to send a message to that group chat.")

            group_mode = True
            # current_group = None
            while group_mode:
                new_msg = client.recv(MSG_LENGTH).decode(FORMAT)
                if '~' in new_msg:
                    # current_group = new_msg[1:]
                    parsed_msg = new_msg.split('~')
                    group(parsed_msg[0], parsed_msg[1])
                    
                elif new_msg == 'exit':
                    group_mode = False
                else:
                    send_to_client(client, "Incorrect format, direct message not sent")
    
        else:
            broadcast(f'[{time.strftime("%d/%m/%y %H:%M:%S")}] {users[username]["username"]}: {message}')

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

        thread = threading.Thread(target=client_handler, args=(client, address,  ))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


# if __name__ == "__main__":
#     main()

print("[STARTING] Server is starting.....")
start()
