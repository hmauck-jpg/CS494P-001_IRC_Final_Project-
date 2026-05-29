

# Haleah Mauck 
# / /2026
# CS-494P-001 Spring 2026
# Final Project  
# Hmauck@pdx.edu
# This is the implemenation of the IRC client

# Import modules 
import socket 
import threading 
import time
import curses 
 

HOST = '127.0.0.1'
PORT = 5000
SHUTDOWN = False


# implement ncurses (maybe later use Vue)
# replaces print and input

  
      
# Desc: Listens for messages from the server
# Input: Client socket connected to the server
# Return: Void
def listenServer(client):
    global SHUTDOWN
    while not SHUTDOWN:
        try:
            message = client.recv(2048).decode('utf-8') 
            # throws exception if client is already closed 
            if not message:
                print("Server closed the connection")
                SHUTDOWN = True
                break 
            
            # just directly print whatever the server sends, it should be 
            # formatted as intended 
            print(f"\n{message}")
       
        except Exception:
            if not SHUTDOWN:
                print("\nDisconnected from server.")
            SHUTDOWN = True
          


# Desc:  
# Input: 
# Return: 
def messageServer(client):
    global SHUTDOWN 
    while not SHUTDOWN:
        try:
            # Get message from input, encode and send the message to the server
            message = input("Enter message to the server: ")
            # throws error when main thread exits 
            if message != '':
                client.sendall(message.encode())
                # throws an exception if client is closed

            else:
                print("Message is empty")
        except (KeyboardInterrupt, EOFError):
            print("You are being dissconnected from the server")
            SHUTDOWN = True
          
     
  


def main():
    global SHUTDOWN

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
        exit(0)
 
    
    threading.Thread(target=listenServer, args=(client, ), daemon=True).start()
    threading.Thread(target=messageServer, args=(client, ), daemon=True).start() 
     
    try:
        while not SHUTDOWN:
            time.sleep(0.1)
    except KeyboardInterrupt:
        SHUTDOWN = True



    client.close()
    print("Thank you for stopping by!")
    exit(0)



if __name__=='__main__':
    main()

   