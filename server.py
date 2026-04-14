

# How do I make an application that starts the server as soon as the first 
# client wants to join, and ends it as soon as the last client disconnects?
# is this possible? does the server need to run infintely on my computer?
# how is this managed by an application?

# how do I conceptulize and code chat rooms? Does this require partioning the server?
# or do I hold an array, and add a number each time a client creates a room
# and then alter each function, to pass as an arugment, which room the function is being called from?


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

# Desc:
# Input:
# Return: 
def client_handler(client):
# client object is returned everytime server connects a client 
    pass


# Desc: Sends a message to all clients connected to the server
# Input:
# Return: 
def messageAll(fromUser, message):
    pass

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


