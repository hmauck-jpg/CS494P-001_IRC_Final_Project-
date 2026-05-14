
 

from IRCFinalProject.server import currentClient

       

# Chats class
        # data

        # list of all chatroom objects
         
        # functions 

        # leave(currentClient bye)
            # messageAll, client has left chat, bye.getCurrentRoom, client has left chat 
            # delete this client from all chatrooms
            # if any chatroom lists this client as creator, creator becomes none
            # if clients in chatroom is empty, size is 0, delete this chatroom from the list 

        # add(currentClient, roomname)
            # checks list of chatroom objects for name
            # adds client to the list of currentClients for theroom when match found

        # create(currentClient hello, string name)
            # create new chatroom object, empty list of clients, creator = hello
            # add to list of chatrooms 

        # delete(string name)
            # send message to all clients in list of clients, chat room is ending
            # delete room from list 


class chats:

    def __init__(self, newChatrooms):
        self._chatrooms = newChatrooms

    # wait, there should be a difference between leaving a room, and leaving the server, is there?
    # if gone is true, the function is called becuase client left the server, if false, the client is just leaving the room

    def leave(bye: currentClient, gone: bool):
        # send bye.getCurRoom() to message all, with bye.getUsername() has left the chat
        # bob = bye.getCurRoom().leave(currentClient, gone)


      
        # case 1 and 2 bob = 3, need to remove creator AND delete chatroom
        # case 1 bob = 1, need to remove creator
        # case 2 bob = 2, need to delete chatroom


           # for chatroom in chatrooms 
            # if chatroom.getCreator() == bye
                # chatroom.setCreator()

        
    def add(addClient: currentClient, chatname):

    def create(hello: currentClient, chatname):

    def delete(chatName):





# chatroom object
    # data
            
        # list of currentClients in room
        # creator currentClient object
        # name string

    # functions 

    # setters + getters

    # delete client
    # takes in client object, if the client exists, in list, remove from list return 0
    # if client was the creator, set creator to none, return 1 
    # if client was the last in chatroom, return 2, and calling function will call delete chatroom

class chatRoom:

    def __init__(self, newCurrentClients, newCreator, newName):
        self._currentClients = newCurrentClients
        self._creator = newCreator
        self._name = newName

    def deleteClient(delClient: currentClient, gone: bool):
        # remove client from list, bob = 0
        if creator == delClient and gone:
            creator = None
            bob = 1
        # if currentClients is now empty, bob += 2, and calling function will call delete chatroom

        # case 1 and 2 bob = 3, need to remove creator AND delete chatroom
        # case 1 bob = 1, need to remove creator
        # case 2 bob = 2, need to delete chatroom
       
            
        return bob

    
