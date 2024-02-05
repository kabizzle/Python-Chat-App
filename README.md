# A basic chat app built in Python

## Developed by Kabir Bissessar for the course ELEC-C7420 Basic Principles of Networking

### Features include: 
1) Message delivery:
- One client should be able to send messages to multiple clients and to receive messages from multiple clients. For example, if there are 3 clients, A, B and
C, Client A can send a message to either B or C, and can receive messages from either B or C. Make sure the messages can be delivered to the right receivers,
and correctly displayed on both the sender and receiver sides.

- The sender will be notified if the messages have been sent successfully or not.

- Accept requests from both IPv4 and IPv6 clients.

- It is not required to implement graphical user interface. You can choose to implement the service using either TCP or UDP socket. 
There are two ways to implement the service. You can choose to implement the server in either way described below.

  - Every message is sent to the server and then forwarded to the receiver. This is recommended as it makes totally asynchronous communication 
  (in which 2 communicating clients are never online at the same time) easy to implement and to maintain.

  - Every message is sent directly from one client to another. In this case, the sender needs to query the network address of the receiver.

2) Group Chat:

- The client which creates a group is the owner of the group and has the rights to rename the group and to manage the member list.

- Any client within a group can send one message simultaneously to the whole group.

- The receivers within a group can see the sender and the group name of any received message.

3) Offline messages:

- The sender is informed if the receiver is offline. The sender can see when a receiver last was online. The server can buffer and forward the messages to the
receiver when the receiver gets connected again.

- The sender can see if the receiver has read his/her message.

### How to start app:

- Navigate to directory containing server.py and client.py
- The following command starts the server instance
```
python3 server.py
```
- Client instances can be started with the following command:
```
python3 client.py
```

> Python command may be different on different machines, e.g. python3 | python | py

When in a client instance:

- The command `/direct` will enter the client into direct message mode 
  - In direct message mode, send a direct message to other users using the syntax `[username]~[message]`
  - The command `/exit` will exit the client back to general mode

- The command `/group` will enter the client into group chat mode
  - When entering group chat mode, the client can create a group by selecting 'y' on the first prompt
  - The name of the group chat can be set at this point
    - It is not currently possible to change the name of a group chat after its creation
  - Users can then be added to the group via the syntax `[username]~[username]~...`
  - In group chat mode, messages can be sent using the syntax `[group name]~[message]`
  - The command `/exit` will exit the client back to general mode
  
- The command `/leave` will cause the client to exit the server
  - Messages that the user receives while not connected to the server will be stored in a queue
    - These unread messages will be sent to the user the next time they connect to the server
  - This command does not close the client well in the terminal, so the terminal window may need to be restarted to enter the computer's terminal

> The server instance does not exit properly, so the terminal window may need to be closed.