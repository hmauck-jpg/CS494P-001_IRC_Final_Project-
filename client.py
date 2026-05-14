

# Haleah Mauck 
# / /2026
# CS-494P-001 Spring 2026
# Final Project  
# Hmauck@pdx.edu
# This is the implemenation of the IRC client

# Import modules 
import socket 
import threading 

HOST = '127.0.0.1'
PORT = 1234

# fix all this TERRIBLE FORMANTTING later when implement ncurses

# Desc: Listens for messages from the server
# Input: Client socket connected to the server
# Return: Void
def listenServer(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if not message:
                raise ConnectionResetError
            
            # just directly print whatever the server sends, it should be 
            # formatted as intended 
            print(f"\n{message}")
       
        except:
            print("\nDisconnected from server.")
            client.close()
            break

# Desc:  
# Input: 
# Return: 
def messageServer(client):
    while 1:
        # Get message from input, encode and send the message to the server
        message = input("Enter message to the server: ")
        if message != '':
            client.sendall(message.encode())

        else:
            print("Message is empty")
            exit(0)
 

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