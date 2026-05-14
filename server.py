

# How do I make an application that starts the server as soon as the first 
# client wants to join, and ends it as soon as the last client disconnects?
# is this possible? does the server need to run infintely on my computer?
# how is this managed by an application?

# how do I conceptulize and code chat rooms? Does this require partioning the server?
# or do I hold an array, and add a number each time a client creates a room
# and then alter each function, to pass as an arugment, which room the function is being called from?

# is a database keeping message history between individual clients
# and all messages sent within a database until it is deleted, nessecary? 
# does there need to be functionality to send a message to a client 
# who is not currently connected? does this need to be stored in a database and 
# sent as soon as they connect to the server? 
# would this database know if they deleted their account? 
# would a user have the ability to 'clear' their own database of messages that will never be sent? 

# do I need mutexes? why is there threading going on here without mutexes?


# No databases of user logins, message history, queued messages
# IRC happens only in real time
# I start and stop the server, doesn't need to start and stop itself 
# multiple clients can connect
# client connects
# client enters a username 
# client is given option menu
# a client can:
# list all avalible rooms 
# join any avalible room
# create a new room
# delete a room they have created
    # if no users are in a room, the room is automaticlly deleted 
    # if they select delete, a list of rooms they have created is displayed to them


# in main

# client handler 
    # listens for connection
    # gets username 
    # creates currentClient object, sends to serverManagement.connectClient(name, currentClient)





# server management class  
    # data

    # a Chats object 

    # MAYBE no index, chatrooms have only a name
    # the current chatroom that a client is in, is a string in the currentClientObject
    # messageAll, loops through the client objects, calls checkChatroom(roomName)
    # if that is the name of the chatroom they are in, it sends the name to them

    # list of all currentClient objects

    # functions 

    # dissconnectClient(currentClient)
        # call client objects deleteClient function 
        # call chatroom list, delete(client)

    # connectClient(name, currentClient)
        # add currentClient to clients list 
        # call listenToClient in thread 

    # listenToClient (currentClient)
        # while 1 
        # try message = client.recv(2048).decode("utf-8")
       

        # while currentClient.getCurrentRoom != none
            # takes input in message:
            # if input != leave 
                # messageAll(currentClient.getCurrentRoom(), message)
            # else
                # myChats.leave(currentClient.getCurrentRoom())
                # currentClient.setCurrentRoom(none)

         # while input != leave server
            # print menu 
    
            # list all avalible rooms 
                # call myChats.list()
                # doesn't break loop
            # join any avalible room
                # call add(currentClient, roomname)
            # create a new room
                # get room name
                # call function to create room with currentClient, name
                # set currentClient current room to created room 
            # leave server 
                # call disconnectClient(currentClient)
            # if the currentClient.creations != null
                # delete a room they have created
                    # doesnt break loop

        # except 
           # call dissconnectClient(currentClient)



# currentClient object class 
        # data

        # client socket object
        # client self selected username 
        # list of index, or room that they created, or -1 if no created rooms? 
        # index of room they are within 

        # functions 

        # DeleteClient function, client disconnects from server
            # their created rooms are updated to orphan 
            # object data deleted

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

# chatroom object
    # data
            
        # list of currentClients in room
        # creator currentClient object
        # name string

    # functions 



# how does a client tell the room it's in, that it disconnected?
# the server is checking to see if client is still connected
# where is that listenMessage loop happening? 
# listenMessage needs to happen in a thread
# where do we call it from in ensure resource protection? 
# each time a client inputs username, and connects to the server, a new object is added to the currentClients list
# as initilization, the currentClients list, passes each object, using a thread, into a listenMessage function 
# any instruction the client sends, comes from the listen message function?
    
 







 


# Haleah Mauck 
# / /2026
# CS-494P-001 Spring 2026
# Final Project  
# Hmauck@pdx.edu
# This is the implemenation of the IRC server  


# Import modules
import socket 
import threading 


HOST = '127.0.0.1' # an IPv4 address
PORT = 1234 # can use any port between 0 to 65535
LISTENERS = 5 # the higher this value, the more resources it will use

active_clients = [] # Currently connected users
# This can ultimately hold an object containing the username
# and any info the server needs to hold about this client 

# Desc:
# Input:
# Return: 
def client_handler(client):
# client object is returned everytime server connects a client 
    
    # Server listens for message from client containing username
    while 1:

        username = client.recv(2048).decode('utf-8')
        # Client object calls function recv, passing in the max size of the message
        # limit the size of the username
        # the   message must be decoded when recived, and encoded when sent 
        if username != '':
            active_clients.append((username, client))
            break
        else:
            print("Client username is empty")


        

    threading.Thread(target=listenMessage, args=(client, username,)).start()


        # The username should be verifed and stored in a database the first time
        # a client logs in
        # this check should be unnessecary, because the username sent should be a 
        # pre stored variable 

# Desc: Listens for any message from connected client 
# sends the message to all connected clients 
# Input: A client who is connected to the server, the username of the client
# Return: 
def listenMessage(client, username): 
    
    while 1:
         
        try:
            message = client.recv(2048).decode("utf-8")
            # listen for a message sent from the client, and decode it

            # this if statement goes inside try block
        
            if message != '':
                # format the username with the message to print
                # should this formatting be the job of a later step? 
                # where should the logic take into account which chat room we are in? 

                # maybe
                # currentClient object sent in
                # call getChadroom, for current chatroom, client is in
                # send message, and chatroom index to messageAll
                toSend = username + ' ~ ' + message
                messageAll(toSend)
            else:
                print(f"The message from the client: {username}, is empty")

        except:
            for user in active_clients:
                if user[1] == client:
                    active_clients.remove(user)
                    break

            client.close()
            messageAll(f"{username} has left the chad")
            break
            # with pre stored username, that should be passed into the function

            

     

# update this function logic later, to reflect 
# message sent in specific chat room or to one other user
# instead of sending a username, sent the client info objec1, sent to the server
# when the client connects
# ask this object for the username, for privacy


# Desc: Sends a message to all clients connected to the server
# Input:
# Return: 
def messageAll(message):
    # iterate through all users in active clients
    for user in active_clients:
        # call individual message function with the client object
        # and the message being sent
        messageIndividual(user[1], message)

# update this function later
# could, have a rooms array, that holds arrays of clients inside each room
# this function could recive the index of the room where the message is being sent
# then loop through all users in rooms[index], and send them the message


# Desc: Sends a message to one other client connected to the server
# Input: Message to send, Client who the message is being sent to
# Return: 
def messageIndividual(client, message):
    client.sendall(message.encode())

# create main 
def main():
    
    # create socket class object 
    # AF_INET 1st paramater means using IPv4, do I need to change this to IPv6?
    # SOCK_STREAM 2nd parameter means using TCP packets (stream)
    # to use UDP use SOCK_DGRAM (datagram)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
         # Pass a double to server, tells the server to this host and port address
        server.bind((HOST, PORT)) 
        print(f"Server is running on host: {HOST}, port {PORT}")
    except:
        print(f"Unable to bind to host: {HOST} and port: {PORT}")

    # Set server limit 
    server.listen(LISTENERS) # The server can accept max of LISTENERS connections at the same time

    # listens infinitely for client connections 
    while 1:
        # listens for a connection from any client 
        client, address = server.accept()
        print(f"Successfully connect to client: {address[0]}, {address[1]}")
        # address is a double, address[0] is the host, address[1] is the port

        # Use threading to handle each client which connects to the server
        # Create a thread, which performs function specified by target (the client handler)
        # pass arguments to the thread in the form of a double specified by args (the client which just connected)
        threading.Thread(target= client_handler, args=(client,)).start()



if __name__=='__main__':
    main()
# means main only runs when script is run directly 
# main will NOT run when script is imported as a module 











# currentClient object class 
        # data

        # client socket object
        # client self selected username 
        # list of index, or room that they created,or name of room, or -1 if no created rooms? 
        # index of room they are within 

        # functions 

        # DeleteClient function, client disconnects from server
            # their created rooms are updated to orphan 
            # object data deleted

        # setters + getters 


class currentClient:

    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def __init__(self, newClientSocket, newUsername, newCreated, newInRoom):
        self._clientSocket = newClientSocket
        self._userName = newUsername
        self._created = newCreated
        self._inRoom = newInRoom


