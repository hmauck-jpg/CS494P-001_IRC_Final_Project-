
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
PORT = 5000 # can use any port between 0 to 65535
LISTENERS = 5 # the higher this value, the more resources it will use
 
  
 
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
                newClient = currentClient(newClientSocket, newUsername, None)  
                self._activeClients.append(newClient)
            else:
                print("Client username is empty")
                # disconnect client, make them try again
                newClientSocket.sendall("Username cannot be empty".encode())
                newClientSocket.close()
                # will this effectvily kick out the client and make them try again? 
                # or will this start a thread with a closed client socket object?

            # Use threading to handle each client which connects to the server
            # Create a thread, which performs function specified by target (the listen function)
            # should I send instead, activeClients, at the index just appended to? 
            threading.Thread(target=self._listen, args=(newClient,)).start()
  
 
    # Desc:
    # Input:
    # Return: 
    def _listen(self, bob: currentClient):

        
        # menu needs to print EVERYTIME user leaves a chatroom
        # loop runs until exception 
        # each time, if/else 
        # every if case, bob is sending a message in a chatroom
        # every time we hit the else case, the menu print should happen again

        # 2 ways to do this

        # call all the functions, like they were called before the loop started
        # write a callMenu function 
        # callMenu(bob)
        # sends what would you like to do?
        # calls join, create, list, and delete with only bob
        # sends leave the server info text

        # alter all of the functions, so they ONLY serve one purpose
        # join(self, bob, toJoin)
        # list(self, bob, toList)
        # delete(self, bob, toDelete)
        # create(self, bob, toCreate)
        # write a menu function, 
        # menu(bob)
        # prints all menu info
        # access chatrooms with lock to print existing chatrooms, only Critical section 
        # would need to delete chatrooms with < 1 member  
 
        bob.getClientSocket().sendall("What would you like to do?".encode())

        self._join(bob)

        self._create(bob)

        bob.getClientSocket().sendall("(3) Leave the server".encode())

        self._list(bob)

        self._delete(bob)


 
        
        while 1: 

            try:
                input = bob.getClientSocket().recv(2048).decode("utf-8")
                print(f"Try to get input from {bob.getUsername()}") # debug 
                
                if bob.getInroom():
                    print(f"{bob.getUsername()} is in room {bob.getInroom()}") # debug
                    if input == "i go bye bye now":
                        self._leave(bob, False)
                    else:
                        self._message(bob, bob.getInroom(), input)

                else:
                    option = input[0]
                    print(f"{bob.getUsername()} not in room, option = {option}") # debug

                    # 1 join
                    if option == "1":
                        newRoom = input[2:]  
                        print(f"newRoom = {newRoom}") # debug

                        if self._join(bob, newRoom):
                            self._message(bob, bob.getInroom(), "Hi eveybody i here now")
                            enterMessage = "You are now in room " + bob.getInroom().getRoomName()
                            print(f"enterMessage = {enterMessage}") # debugS
                            bob.getClientSocket().sendall(enterMessage.encode())
                        else:
                            bob.getClientSocket().sendall("This room no longer exists!".encode())

                    # 2 create
                    elif option == "2":
                        createdRoomName = input[2:]
                        print(f"createdRoomName = {createdRoomName}") # debug
                        # This needs to happen first!!
                        # if a chat exists in chatrooms, with no users
                        # it might be deleted by another thread 
                        createdRoom = chatroom(createdRoomName, 1)
                        print(f"Calling create with createdRoom = {createdRoom}") # debug
                        self._create(bob, createdRoom)

                        # Tell the client where they are now 
                        enterMessage = "You are now in room " + bob.getInroom().getRoomName()
                        print(f"enterMessage = {enterMessage}")
                        bob.getClientSocket().sendall(enterMessage.encode())
                         
                    # 3 leave
                    elif option == "3":
                        self._leave(bob)
                        break 

                    # 4 list
                    elif option == "4":
                        toList = input[2:]
                        print(f"toList = {toList}") # debug
                        self._list(bob, toList)

                    # 5 delete
                    elif option == "5":
                        toDelete = input[2:]
                        if bob.getCreated():
                            for creation in bob.getCreated():
                                if creation == toDelete:
                                    self._delete(bob, toDelete)
                        else:
                            bob.getClientSocket().sendall("You haven't created any chatrooms!".encode())
            
            except: 
                self._leave(bob, True)
                break 

    
    # Desc:
    # Input:
    # Return: 
    def _delete(self, bob, toDelete=None):
        if toDelete:
            # CRITICAL SECTION
            with self._lock:
                for chat in self._chatrooms:
                    if chat.getRoomName() == toDelete:
                        self._message(bob, toDelete, "Sorry eveybody i end room now bye")
                        self._chatrooms.remove(chat)
        else:
            if bob.getCreated():
                bob.getClientSocket().sendall("(4) Delete your own chat room".encode())
                # print all bob's created chatrooms 
                # this is not critical, because no one except bob, will alter the list bob._created
                for chat in bob.getCreated():
                    bob.getClientSocket().sendall(f"{chat.getRoomName()}".encode())
                bob.getClientSocket().sendall("     *To delete one of your chatrooms, enter: 4 <chatroom_to_delete>".encode())

    
    # Desc:
    # Input:
    # Return: 
    def _join(self, bob, toJoin=None):

        # non critical part of the function, don't lock it
        if not toJoin:
            bob.getClientSocket().sendall("(1) Join an existing chat room".encode())
            bob.getClientSocket().sendall("     *To join enter: 1 <name_of_room_to_join>".encode())
            counter = 0

            # CRITICAL SECTION
            with self._lock:
                # list all avalible rooms
                print(f"listing chat rooms") # debug
                bob.getClientSocket().sendall("Existing chatrooms:".encode())
                for chat in self._chatrooms:
                    print(f"{chat.getRoomName()}: {chat.getUsers()}") # debug
                    if chat.getUsers() < 1:
                        self._chatrooms.remove(chat)
                    else:
                        toPrint = "    " + chat.getRoomName()
                        bob.getClientSocket().sendall(toPrint.encode())
                        counter += 1

            if counter < 1:
                bob.getClientSocket().sendall("     Nothing here!".encode())
    

        else:
            # CRITICAL SECTION
            with self._lock:
            
                for chat in self._chatrooms:
                    if chat.getRoomName() == toJoin: 
                        chat.increment() 
                        bob.setInroom(chat)
                        print(f"chat = {chat} bob inRoom = {bob.getInroom()}") # debug
                        return True
                
                bob.setInroom(None)
                return False 
               
        
                 
         
    # Desc:
    # Input:
    # Return: 
    def _create(self, bob, toCreate=None):
        
        if toCreate:
            print(f"toCreate = {toCreate}") # debug
            bob.setInroom(toCreate)
            bob.addCreated(toCreate.getRoomName())
            # CRITICAL SECTION 
            with self._lock:
                self._chatrooms.append(toCreate)
                print(f"chatrooms after append:") # debug
                for chat in self._chatrooms: # debug
                    print(f"{chat.getRoomName()}") # debug

        else:
            bob.getClientSocket().sendall("(2) Create a new chat room".encode())
            bob.getClientSocket().sendall("    *To create enter: 2 <name_of_your_new_chatroom>".encode())
        
         
    # Desc:
    # Input:
    # Return: 
    def _leave(self, bob: currentClient, gone: bool):
        print(f"client {bob} is leaving") # debug
        # need to leave existing chatroom
        leaveMessage = " i go bye bye now"
        self._message(bob, bob.getInroom(), leaveMessage)
         
        # CRITICAL SECTION
        with self._lock:
            for chat in self._chatrooms:
                if chat == bob._inroom:
                    chat.decrement()
                    break 
        bob.setInroom(None)
        bob.getClientSocket().sendall("You have left the chatroom".encode())

        if gone:
            bob.getClientSocket().sendall("You are being disconnected from the server".encode())
            bob.getClientSocket().close()
        # CRITICAL SECTION 
            with self._lock:
                for user in self._activeClients:
                    if user == bob:
                        self._activeClients.remove(user)
                        break  

    # Desc:
    # Input:
    # Return: 
    def _list(self, bob, toList=None):
            if toList:
                count1 = 0

                # CRITICAL SECTION
                with self._lock:
                    # list members in chatroom toList
                    for user in self._activeClients:
                        print(f"{user.getUsername()}: {user.getInroom()}") # debug
                        if user.getInroom():
                            if user.getInroom().getRoomName() == toList:
                                count1 += 1
                                message1 = "    " + user.getUsername()
                                bob.getClientSocket().sendall(message1.encode())
                print(f"count1 = {count1}")
                if count1 < 1:
                    bob.getClientSocket().sendall("It looks like this room doesn't exist anymore!".encode())

                print("Returning from list") # debug
            else:
                bob.getClientSocket().sendall("(4) List members in an existing chatroom".encode())
                bob.getClientSocket().sendall("     *To list chatroom members enter: 4 <name_of_chatroom>".encode())
                 
        
    
    # Desc:
    # Input:
    # Return: 
    def _message(self, bob, room: chatroom, message):

        formatMessage = bob.getUsername() + " ~ " + message
        print(f"formatMessage = {formatMessage}") # debug

      
        # CRITICAL SECTION
        with self._lock:
            print(f"getting recipients, room = {room.getRoomName()}") # debug
            recipients = [u for u in self._activeClients if u.getInroom() == room]

        print(f"{recipients}") # debug
        # Don't lock message sending!
        for user in recipients:
            print(f"sending to {user.getUsername()}") # debug
            user.getClientSocket().sendall(formatMessage.encode())


# currentClient object class 
class currentClient:


    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def __init__(self, newClientSocket, newUsername, newInroom: chatroom):
        self._clientSocket = newClientSocket
        self._username = newUsername
        self._created = []
        self._inroom = newInroom

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
    def getUsername(self):
        return self._username

    def addCreated(self, newRoomName):
        self._created.append(newRoomName)

class chatroom:

    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def __init__(self, newRoomName, users: int):
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