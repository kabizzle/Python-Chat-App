import socket
import threading

# HOST = socket.gethostbyname(socket.gethostname())
# HOST = '0.0.0.0'
# PORT = 5678
# SERVER_CONFIG = (HOST, PORT)
HOST_INFO = socket.getaddrinfo('localhost', 8080)
SERVER_CONFIG_IPv4 = HOST_INFO[1][4]
SERVER_CONFIG_IPv6 = HOST_INFO[0][4]
FORMAT = 'utf-8'
MSG_LENGTH = 2048
DIRECT_MSG = '/direct'
GROUP_MSG = '/group'
DISCONNECT_MSG = '/leave'
WELCOME_MSG = f"Welcome to the server. You can send a message to everyone by just typing :)\nTo send a direct message to another user, send {DIRECT_MSG}. \nTo create a group chat, send {GROUP_MSG}\n"
CONNECTED = False

# Function to listen for messages from server
def listen_to_server(client, CONNECTED):

    # connected = True
    while CONNECTED:
        message = client.recv(MSG_LENGTH).decode(FORMAT)

        if message == DISCONNECT_MSG:
            # connected = False
            CONNECTED = False
        elif message != '':
            # username = message.split(":")[0]
            # content = message.split(":")[1]
            print(message)
        else:
            print("Message received from client is empty")


# Function to send communicate client info with server
def initialise_on_server(client, CONNECTED):

    username = input("Please enter your username: ")

    while username == '':
        print("Username cannot be empty.")
        username = input("Please enter your username: ")

    # if username != '':
    #     client.sendall(username.encode())
    # else:
        # print("Username cannot be empty.")
    
    client.send(username.encode(FORMAT))
    CONNECTED = True
         
    threading.Thread(target=listen_to_server, args=(client, CONNECTED)).start()
    send_message_to_server(client, CONNECTED)


# Function to send message to server
def send_message_to_server(client, CONNECTED):

    while CONNECTED:
        message = input()    

        if message != '':
            client.send(message.encode(FORMAT))


# Main function
def start():

    # Creating client socket object
    ip_type = input(f'[INITIALIZATION] What type of connection would you like to establish? ipv4/ipv6\n')

    if ip_type.lower() == 'ipv6':
        client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        client.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)

        # Attempt to connect to server
        try:
            client.connect(SERVER_CONFIG_IPv6)
            print(f"Client successfully connected to server {SERVER_CONFIG_IPv6} over {ip_type}")
            print(WELCOME_MSG)
        except:
            print(f"Client unable to connect to server {SERVER_CONFIG_IPv6}")
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to connect to server
        try:
            client.connect(SERVER_CONFIG_IPv4)
            print(f"Client successfully connected to server {SERVER_CONFIG_IPv4} over {ip_type}")
            print(WELCOME_MSG)
        except:
            print(f"Client unable to connect to server {SERVER_CONFIG_IPv4}")

    initialise_on_server(client, CONNECTED)

# if __name__ == "__main__":
#     main()

start()