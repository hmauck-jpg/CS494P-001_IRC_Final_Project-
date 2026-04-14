

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

# Import modules 
import socket 
import threading 

HOST = '127.0.0.1'
PORT = 1234

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


if __name__=='__main__':
    main()