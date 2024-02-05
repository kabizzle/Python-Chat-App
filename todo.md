# TODO:
- check if inputted users in server when creating group
- implement file transfer
- implement gui?
- Add README


# KINDA FIXED:
- handle leaving server in client - exit to terminal
- implement read receipts
- the group chat admin can add/remove members, edit group info and delete group 


# DONE:
- show when users leave the server
- when users send dm command, it will only message desired client
- a user can send group chat command to form a group with clients A and B etc.
- implement datetime: 
      when message sent: include time.time() 
      when message received, perform datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
- let users know when added to a group chat
- make creating group chat a command in group mode rather than default
- users can send messages to group even if they didnt create it
- implement message queue to save messages for offline users
- identify direct vs groupchat messages
      copy string format for broadcast message and add 'from [user]' or 'from [group]'
- implement choosing whether to use IPv4 or IPv6
- add 'last online' to user object
- inform senders if sender is offline and when they were last online
