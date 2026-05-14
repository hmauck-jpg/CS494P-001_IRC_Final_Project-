



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
 
 



# create main 
def main():

    # give the user an option to specify the host, port and listenters? 

    myServer = serverManagment(HOST, PORT)

    # how do we handle disconnection from the server? how do we tell all clients the server disconnected?
    # or is a server faliure handled in the client code? 
    
    

if __name__=='__main__':
    main()
# means main only runs when script is run directly 
# main will NOT run when script is imported as a module 



# serverManagment object class
class serverManagment: 
   
    # Desc: Default constructor 
    # Input: 
    # Return: None
    def __init__(self, newHOST, newPORT):
        self._host = newHOST
        self._port = newPORT
        self._activeClients = []
        self._chatrooms = []
        self._lock = threading.Lock()

        # create socket class object 
        # AF_INET 1st paramater means using IPv4, do I need to change this to IPv6?
        # SOCK_STREAM 2nd parameter means using TCP packets (stream)
        # to use UDP use SOCK_DGRAM (datagram)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
             # Pass a double to server, tells the server to this host and port address
            self._server.bind((self._host, self._port)) 
            print(f"Server is running on host: {self._host}, port {self._port}")
        except:
            print(f"Unable to bind to host: {self._host} and port: {self._port}")

        # Set server limit 
        self._server.listen(LISTENERS) # The server can accept max of LISTENERS connections at the same time

        try:
            self._client_handler()
        except KeyboardInterrupt:
            for client in self._activeClients:
                client.getClientSocket().sendall("SERVER_SHUTDOWN".encode())
                client.getClientSocket().close()
            self._server.close()

    # Desc:
    # Input:
    # Return: 
    def _client_handler(self):

         # listens infinitely for client connections 
        while 1:
            # listens for a connection from any client
            # takes client socket object, and double host and port 
            newClientSocket, newAddress = self._server.accept()
            print(f"Successfully connect to client: {newAddress[0]}, {newAddress[1]}")
            # address is a double, address[0] is the host, address[1] is the port

            newUsername = newClientSocket.recv(2048).decode('utf-8')
            # Client object calls function recv, passing in the max size of the message
            # limit the size of the username
            # the  message must be decoded when recived, and encoded when sent 
            if newUsername != '':
                # create new currentClient object
                newClient = currentClient(newClientSocket, newUsername, None, None)  
                self._activeClients.append(newClient)
            else:
                print("Client username is empty")
                # disconnect client, make them try again? 

            # Use threading to handle each client which connects to the server
            # Create a thread, which performs function specified by target (the listen function)
            # should I send instead, activeClients, at the index just appended to? 
            threading.Thread(target=self._listen, args=(newClient,)).start()
  
 
    # Desc:
    # Input:
    # Return: 
    def _listen(self, bob: currentClient):
 
        
        print("What would you like to do?")

        self._join()
        
        print("(2) Create a new chat room")
        print ("    *To create enter: 2 <name_of_your_new_chatroom>")
        
        print("(3) Leave the server")
        
        self._delete(bob)
        
        while 1: 

            try:
                input = bob.getClientSocket().recv(2048).decode("utf-8")
                
                if bob.getInroom():
                    if input == "i go bye bye now":
                        self._leave(bob)
                    else:
                        self._message(bob, bob.getInroom(), input)

                else:
                    option = input[0]

                    # 1 join
                    if option == "1":
                        newRoom = input[1:]  

                        if not self._join(bob, newRoom):
                            print("This room no longer exists!")

                    # 2 create
                    elif option == "2":
                        createdRoomName = input[1:]
                        createdRoom = chatroom(createdRoomName, 1)
                        # This needs to happen first!!
                        # if a member of activeClients is not in a room that exits in chatrooms
                        # it might be deleted by another thread 
                        bob.setInroom(createdRoom)
                        # This needs to happen before we append to chatrooms!
                        # as soon as the chat is in chatrooms, another thread 
                        # might be checking activeClients to see who created a chat
                        bob.addCreated(createdRoomName)
                        # CRITICAL SECTION 
                        with self._Lock:
                            self._chatrooms.append(createdRoom)
                         

                    # 3 leave
                    elif option == "3":
                        self._leave(bob)
                        break 

                    # 4 delete
                    elif option == "4":
                        if bob.getCreated():
                            toDelete = input[1:]
                            self._delete(bob, toDelete)
                        else:
                            print("You haven't created any chatrooms!")
            
            except: 
                self._leave(bob)
                break 

    
    # Desc:
    # Input:
    # Return: 
    def _delete(self, bob, toDelete=None):
        if toDelete:
            # CRITICAL SECTION
            with self._Lock:
                for chat in self._chatrooms:
                    if chat.getRoomName() == toDelete:
                        self._message(bob, toDelete, "Sorry eveybody i end room now bye")
                        self._chatrooms.remove(chat)
        else:
            if bob._getCreated():
                print("(4) Delete your own chat room")
                # print all bob's created chatrooms 
                for chat in bob.getCreated():
                    print(f"{chat}")
                print("     *To delete one of your chatrooms, enter: 4 <chatroom_to_delete>")

    
    # Desc:
    # Input:
    # Return: 
    def _join(self, bob, toJoin=None):
        if toJoin:
            bob.setInroom(toJoin)
            # check if toJoin is in chatrooms, if so, return true, if not, return false
            with self._Lock:
                for chat in self._chatrooms:
                    if chat == toJoin:
                        return True
                
            bob.setInroom(None)
            return False 
               
        else:
            print("(1) Join an existing chat room")
            # CRITICAL SECTION
            with self._Lock:
            # list all avalible rooms
                for chat in self._chatrooms:
                    if chat.getUsers() < 1:
                        self._chatrooms.remove(chat)
                    else:
                        print(f"{chat.getRoomName()}")
            print("     *To join enter: 1 <name_of_room_to_join>")

            # why doesn't it regonize the list varibale chatrooms?
            # use this function to check, and delete, if there is no users in the room 
     
         
    # Desc:
    # Input:
    # Return: 
    def _leave(self, bob: currentClient):

        # need to leave existing chatroom
        leaveMessage = bob.getUsername + " has left the chat"
        self._message(bob, bob.getInroom(), leaveMessage)
        bob.clientSocket.close()
         
        # CRITICAL SECTION
        with self._Lock:
            for chat in self._chatrooms:
                if chat == bob._inroom:
                    chat.decrement()
                    break 

        # CRITICAL SECTION 
        with self._Lock:
            for user in self._activeClients:
                if user == bob:
                    self._activeClients.remove(user)
                    break  
    
    # Desc:
    # Input:
    # Return: 
    def _message(self, bob, room, message):
    
        formatMessage = bob.getUsername() + " ~ " + message

        # CRITICAL SECTION
        with self._lock:
            recipients = [u for u in self._activeClients if u.getInroom() == room]

        # Don't lock message sending!
        for user in recipients:
            user.getClientSocket().sendall(formatMessage.encode())


# currentClient object class 
class currentClient:


    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def __init__(self, newClientSocket, newUsername, newCreated, newInroom):
        self._clientSocket = newClientSocket
        self._username = newUsername
        self._created = newCreated
        self._inRoom = newInroom

    # setters and getters

    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def setInroom(self, newInroom):
        self._inroom = newInroom
 

    # Desc: Constructor with parameters
    # Input: 
    # Return: None  
    def getInroom(self):
        return self._inroom
    
    # Desc: Constructor with parameters
    # Input: 
    # Return: None  
    def getCreated(self):
        return self._created
    
    # Desc: Constructor with parameters
    # Input: 
    # Return: None  
    def getClientSocket(self):
        return self._clientSocket

    # Desc: Constructor with parameters
    # Input: 
    # Return: None  
    def geUsername(self):
        return self._username

    def addCreated(self, newRoomName):
        self._created.append(newRoomName)

class chatroom:

    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def __init__(self, newRoomName, users):
        self._roomName = newRoomName
        self._users = users

    # setters and getters

    # Desc: Gets the roomName
    # Input: None
    # Return: string, the name of the this chatroom 
    def getRoomName(self):
        return self._roomName
    
    # Desc: Gets the number of users in the room
    # Input: None
    # Return: int, the number of users in this room
    def getUsers(self):
        return self._users

    # Desc: Gets the number of users in the room
    # Input: None
    # Return: int, the number of users in this room
    def increment(self):
        self._users += 1

    # Desc: Gets the number of users in the room
    # Input: None
    # Return: int, the number of users in this room
    def decrement(self):
        self._users -= 1


