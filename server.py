

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

active_clients = [] # Currently connect users
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
        # the message must be decoded when recived, and encoded when sent 
        if username != '':
            active_clients.append(username, client)
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
        message = client.recv(2048).decode("utf-8")
        # listen for a message sent from the client, and decode it
        if message != '':
            # format the username with the message to print
            # should this formatting be the job of a later step? 
            # where should the logic take into account which chat room we are in? 
            toSend = username + ' ~ ' + message
            messageAll(toSend)
        else:
            print(f"The message from the client: {username}, is empty")

# update this function logic later, to reflect 
# message sent in specifc chat room or to one other user
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


