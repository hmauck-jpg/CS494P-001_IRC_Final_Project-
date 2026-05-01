

# How do I make an application that will create
# new 'clients' every time someone wants to log in?
# like ask for a username and password, then store their data
# and make a new profile, or connect them to the server
# with an existing username? 
# so that everyone who uses this IRC
# doesn't literally need to have the client code on 
# their computer, how does this work? 
# what kind of data structure do I use? 
# is any of this the job of a GUI?

# add ncurses later, to get rid of formatting issues with messages
# printing in funky places in the terminal 

# print()	window.addstr()
# input()	window.getstr()
# clear()	window.clear()
# \n	window.addstr("\n")


# Import modules 
import socket 
import threading 

HOST = '127.0.0.1'
PORT = 1234



# Desc: Listens for messages from the server
# Input: Client socket connected to the server
# Return: Void
def listenServer(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if not message:
                raise ConnectionResetError

            parts = message.split("~", 1)
            # The message recived, will contain username~content
            # use the split function to create a double 
            # before ~ is the username, and after is the content 

            if len(parts) == 2:
                username, content = parts
                print(f"\n[{username}] {content}")
            
            else:
                # System message (no username)
                print(f"\n{message}")

            # print("Enter message: ", end="", flush=True)

        except:
            print("\nDisconnected from server.")
            client.close()
            break
# fix all this TERRIBLE FORMANTTING later when implement ncurses

# Desc:  
# Input: 
# Return: 
def messageServer(client):
    while 1:
        # Get message from input, encode and send the message to the server
        message = input("Enter message: ")
        if message != '':
            client.sendall(message.encode())

        else:
            print("Message is empty")
            exit(0)

# modify function logic later
# before client enters listening loop, client gets rooms and connected clients listed
# client can join room, create room, or send individual message

# Desc: Send the username to the server, after the client socket has connected
# Input: Client socket which just connected to the server
# Return: Void 
def sendUsername(client):

    # Get username from input and send to the server
    username = input("Enter username: ")
    if username != '':
        client.sendall(username.encode())
    else: 
        print("Username cannot be empty")
        exit(0)

    # start function which listens for messages from server, with thread
    threading.Thread(target=listenServer, args=(client, )).start()

    # call function to allow client to send a message 
    messageServer(client)

# update this function logic
# The client registers with a username and password
# this username and password is stored in a database
# when the client logs in, the stored username is automatically sent to 
# the server without asking for user input 

# does this function have an issue, where you can only send one message
# before you receive a message? 
# you can't choose what you want to do next via a menu? 

def main():

    # create socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # This socket must match the address and port of the server 
    # it is trying to connect to

    # Connect to server
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST}, {PORT}")

    # Pass client socket to sendUsername, gets username from input
    # and sends it to the server 
    sendUsername(client)


if __name__=='__main__':
    main()