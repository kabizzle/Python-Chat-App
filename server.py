import socket
import threading
from queue import Queue
from datetime import datetime

# TODO:
# - check if inputted users in server when creating group
# - add 'last online' to user object
# - inform senders if sender is offline and when they were last online
# - implement file transfer
# ? implement gui
#
#
# KINDA FIXED:
# - handle leaving server in client - exit to terminal
# - implement read receipts
# - the group chat admin can add/remove members, edit group info and delete group 
#
#
# DONE:
# - show when users leave the server
# - when users send dm command, it will only message desired client
# - a user can send group chat command to form a group with clients A and B etc.
# - implement datetime: 
#       when message sent: include time.time() 
#       when message received, perform datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
# - let users know when added to a group chat
# - make creating group chat a command in group mode rather than default
# - users can send messages to group even if they didnt create it
# - implement message queue to save messages for offline users
# - identify direct vs groupchat messages
#       copy string format for broadcast message and add 'from [user]' or 'from [group]'
# - implement choosing whether to use IPv4 or IPv6

HOST = ""
PORT = 8080
SERVER_CONFIG_IPv4 = (HOST, PORT)

FORMAT = 'utf-8'
MSG_LENGTH = 2048
DIRECT_MSG = '/direct'
GROUP_MSG = '/group'
DISCONNECT_MSG = '/leave'
GENERAL_MSG = f"[GENERAL] Send message to everyone by just typing :)\nCommands: '{DIRECT_MSG}' '{GROUP_MSG}' '{DISCONNECT_MSG}'"


# Template for storing client data in dictionary
user = lambda username, socket, online : {"username": username, "client": socket, "online": online, "last-online": None, "queue": Queue()}

# list of clients connected to server
users = {} 

# list of group chats in server
groups = {}


# Function to send message to a single client
def send_to_client(client, message, sender=None, receiver=None):
    client.send(message.encode(FORMAT))
    if sender and receiver:
        sender.send(f"[seen by {receiver}]\n".encode(FORMAT))


# Function to send messages to all active clients
def broadcast(message, sender):
    client_list = []
    for client in users.keys():
        if users[client]["online"]:
            send_to_client(users[client]["client"], message)
            if sender and sender is not users[client]["client"]:
                client_list.append(users[client]["username"])
        else:
            users[client]["queue"].put((message, sender))
            if sender:
                sender.send(f'[*sent*]\n[{client} offline. Last online {users[client]["last-online"].strftime("%d/%m/%y %H:%M:%S")}]\n'.encode(FORMAT))

    if sender and client_list != []:
        sender.send(f"[*sent*]\n[seen by {client_list}]\n".encode(FORMAT))


def direct(username, message, sender):
    if username in users.keys():
        if users[username]["online"]:
            send_to_client(users[username]["client"], message)
            if sender:
                sender.send(f"[*sent*]\n[seen by {username}]\n".encode(FORMAT))
        else:
            users[username]["queue"].put((message, sender))
            if sender:
                sender.send(f'[*sent*]\n[{username} offline. Last online {users[username]["last-online"].strftime("%d/%m/%y %H:%M:%S")}]\n'.encode(FORMAT))


def group(group_name, message, sender):
    client_list = []
    group_users = groups[group_name]["users"]
    for member in group_users:
        if users[member]["online"]:
            send_to_client(users[member]["client"], message)
            if sender and sender is not users[member]["client"]:
                client_list.append(member)
        else:
            users[member]["queue"].put((message, sender))
            if sender:
                sender.send(f'[*sent*]\n[{member} offline. Last online {users[member]["last-online"].strftime("%d/%m/%y %H:%M:%S")}]\n'.encode(FORMAT))
    if sender:
        sender.send(f"[*sent*]\n[seen by {client_list}]\n".encode(FORMAT))


def create_group(group_name, usernames, admin):
    groups[group_name] = {"users": usernames, "admin": admin}


def check_user_groups(username):
    group_list = []
    for group in groups.keys():
        if username in groups[group]["users"]:
            group_list.append(group)
    
    return group_list


def client_handler(client, address):
    print(f"[SERVER] User {address} connected")
    connected = True
    
    username = client.recv(MSG_LENGTH).decode(FORMAT)
    if username in users.keys():
        users[username]["client"] = client
        users[username]["online"] = True
    else:
        users[username] = user(username, client, True)
    
    broadcast(f"[SERVER] {username} has joined the server.", sender=None)

    while connected:
        send_to_client(client, GENERAL_MSG, sender=None)
        while not users[username]["queue"].empty():
            q_msg, q_sender = users[username]["queue"].get()
            send_to_client(client, f'{q_msg} \n', q_sender, username)
        message = client.recv(MSG_LENGTH).decode(FORMAT)
        current_time = datetime.now()
        time = current_time.strftime("%d/%m/%y %H:%M:%S")

        if message == DISCONNECT_MSG:
            send_to_client(client, "/leave")
            connected = False
            client.close()
            users[username]["client"] = None
            users[username]["online"] = False
            users[username]["last-online"] = datetime.now()
            broadcast(f"[SERVER] {username} has left the server.", sender=None)

        elif message == DIRECT_MSG:
            send_to_client(client, "[DIRECT] You have entered direct message mode!\nDirect message to a user by '[username]~[message]'\n'/exit' to return to general\n")
            direct_mode = True
            while direct_mode:
                new_msg = client.recv(MSG_LENGTH).decode(FORMAT)
                if '~' in new_msg:
                    parsed_msg = new_msg.split('~')
                    direct_msg = f'[DIRECT] [{time}] {users[username]["username"]} sent you: {parsed_msg[1]}\n'
                    direct(parsed_msg[0], direct_msg, sender=client)
                elif new_msg == '/exit':
                    direct_mode = False
                else:
                    send_to_client(client, "[DIRECT] Incorrect format, direct message not sent\n Direct message to a user by '[username]~[message]'\n'/exit' to return to general\n")
        
        elif message == GROUP_MSG:
            send_to_client(client, "[GROUP] You have entered group chat mode!", sender=None)
            user_groups = check_user_groups(username)
            send_to_client(client, f"[GROUP] You are a member of groups: {user_groups}\n")

            send_to_client(client, "[GROUP] Would you like to create a new group? y/n", sender=None)
            resp = client.recv(MSG_LENGTH).decode(FORMAT)
            if resp == "y":
                send_to_client(client, "[GROUP] Group name:", sender=None) 
                group_name = client.recv(MSG_LENGTH).decode(FORMAT)
                send_to_client(client, "[GROUP] Add users to group using format '[username]~[username]~...'", sender=None)
                group_users = client.recv(MSG_LENGTH).decode(FORMAT)
                parsed_group_users = group_users.split('~')
                parsed_group_users.append(username)
                
                create_group(group_name, parsed_group_users, username)

                group(group_name, f"[GROUP] You have been added to group {group_name}!\n", sender=client)

            user_groups = check_user_groups(username)
            send_to_client(client, f"[GROUP] You are a member of groups: {user_groups}\n")

            group_mode = True
            while group_mode:
                send_to_client(client, "[GROUP] Commands: '[group name]~[message]' '/kick [username]' '/add [username]' '/exit'")

                new_msg = client.recv(MSG_LENGTH).decode(FORMAT)
                if '~' in new_msg:
                    parsed_msg = new_msg.split('~')
                    group_msg = f'[GROUP] [{time}] {users[username]["username"]} sent to group {parsed_msg[0]}: {parsed_msg[1]}'
                    group(parsed_msg[0], group_msg, sender=client)
                elif new_msg == '/exit':
                    group_mode = False
                elif '/add' in new_msg:
                    new_user = new_msg.split(' ')
                    if new_user not in groups[group_name]["username"]:
                        groups[group_name]["usernames"].append(new_user)
                        group(group_name, f"[GROUP] {new_user} has been added to group {group_name}!", sender=None)
                    else:
                        send_to_client(client, "[GROUP] User already in group\n")
                elif '/kick' in new_msg:
                    kicked_user = new_msg.split(' ')
                    if kicked_user in groups[group_name]["username"]:
                        groups[group_name]["usernames"].remove(kicked_user)
                        group(group_name, f"[GROUP] {kicked_user} has been removed from group {group_name}!\n", sender=None)
                        send_to_client(users[kicked_user]["client"], f"[GROUP] You have been removed from group {group_name}!\n")

                else:
                    send_to_client(client, "[GROUP] Incorrect format, direct message not sent")
    
        else:
            broadcast(f'[GENERAL] [{time}] {users[username]["username"]}: {message}', sender=client)

        print(f"{address}: {message}")
    
    client.close()
    users[username]["client"] = None
    users[username]["online"] = False
    users[username]["last-online"] = datetime.now()


# Main function
def start():

    # Attempts to create server at given HOST IP and PORT
    server = socket.create_server(SERVER_CONFIG_IPv4, family=socket.AF_INET6, dualstack_ipv6=True)

    try:
        # server.bind(SERVER_CONFIG_IPv4)
        print(f"[RUNNING] Server is running at {SERVER_CONFIG_IPv4} and accepts both IPv4 and IPv6 connections")
    except:
        print(f"[ERROR] Server unable to be created at host {SERVER_CONFIG_IPv4}")

    print(f"[LISTENING] Server is listening on {SERVER_CONFIG_IPv4}")

    # Listen for clients
    server.listen()
 
    while True:
        client, address = server.accept()
        print(f"Client {address[0]} {address[1]} successfully connected to server!")

        thread = threading.Thread(target=client_handler, args=(client, address,  ))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting.....")
start()
