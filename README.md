How to start app:
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

- The command '/direct' will enter the client into direct message mode 
  - In direct message mode, send a direct message to other users using the syntax "[username]~[message]"
- The command '/group' will enter the client into group chat mode
  - When entering group chat mode, the client can create a group by selecting 'y' on the first prompt
  - The name of the group chat can be set at this point
    - It is not currently possible to change the name of a group chat after its creation
  - Users can then be added to the group via the syntax "[username]~[username]~..."
  - In group chat mode, messages can be sent using the syntax "[group name]~[message]"
  - The command '/exit' will exit the client back to general mode
