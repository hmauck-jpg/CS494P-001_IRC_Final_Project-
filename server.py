
# Haleah Mauck 
# / /2026
# CS-494P-001 Spring 2026
# Final Project  
# Hmauck@pdx.edu
# This is the implemenation of the IRC server  


# Import modules
import socket 
import threading 
import traceback 


HOST = '127.0.0.1' # an IPv4 address
PORT = 4000 # can use any port between 0 to 65535
LISTENERS = 5 # the higher this value, the more resources it will use
  
# add an option to manually change host and port, so grader can run it on whatever works
 
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
            # adjust this to account for client keyboard interupts 
        except KeyboardInterrupt:
            for client in self._activeClients:
                client.getClientSocket().sendall("SERVER_SHUTDOWN".encode())
                client.getClientSocket().close()
            self._server.close()
 
    
    # Desc: Listens infinitely for client connections, creates a new currentClient object
    # sends this object to getUsername in a thread 
    # Input: None
    # Return: None
    def _client_handler(self):

        while 1:
            newClientSocket, newAddress = self._server.accept()
            newClient = currentClient(newClientSocket, None, None)
            threading.Thread(target=self._getUsername, args=(newClient,)).start()
 

     
    # Desc: Gets a username from the new client, and calls listen with the new currentClient object
    # Input: new currentClient object
    # Return: None
    def _getUsername(self, newClient: currentClient):
     
        try:
            self._message(newClient, None, "Enter username: ")
            # if this message is sent to a dead client, leave will be called and close the client socket 
            newUsername = newClient.getClientSocket().recv(2048).decode('utf-8')

            if newUsername == '':
                self._message(newClient, None, "Username cannot be empty. Please retry connection!")
                self._leave(newClient, True)

            else:
                newClient.setUsername(newUsername)
                self._activeClients.append(newClient)
                print(f"Sending {newClient.getUsername()} to listen") # debug
                self._listen(newClient)
                
        except:
            self._leave(newClient, True)

         

 

    # Desc:
    # Input:
    # Return: 
    def _listen(self, bob: currentClient):

        
        while 1: 

            try:

                if not bob.getInroom():
                    self._menu(bob)

                input = bob.getClientSocket().recv(2048).decode("utf-8")
                print(f"Try to get input from {bob.getUsername()}") # debug 
                
                if bob.getInroom():
                    print(f"{bob.getUsername()} is in room {bob.getInroom()}") # debug
                    if input == "i go bye bye now":
                        sayGoodbye = self._leave(bob, False)
                        # send left the chat message to old chatroom
                        self._message(bob, sayGoodbye, input) 
                        # send left the chat message to the client bob
                        self._message(bob, None, "You have left the chatroom")
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
                            print(f"enterMessage = {enterMessage}") # debug
                            self._message(bob, None, enterMessage)
                        else:
                            self._message(bob, None, "This room no longer exists!")

                    # 2 create
                    elif option == "2":
                        createdRoomName = input[2:]
                        print(f"createdRoomName = {createdRoomName}") # debug
                        # This needs to happen first!!
                        # if a chat exists in chatrooms, with no users
                        # it might be deleted by another thread 
                        createdRoom = chatroom(createdRoomName, 1)
                        print(f"Calling create with createdRoom = {createdRoom}") # debug
                        if self._create(bob, createdRoom):

                            # Tell the client where they are now 
                            enterMessage = "You are now in room " + bob.getInroom().getRoomName()
                            print(f"enterMessage = {enterMessage}")
                            self._message(bob, None, enterMessage)
                        else: 
                            self._message(bob, None, f"Sorry! chatroom {createdRoomName} already exists")
                         
                    # 3 leave
                    elif option == "3":
                        # send disconnect message to client bob
                        self._message(bob, None, "You are being disconnected from the server")
                        self._leave(bob, True)
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
                            self._message(bob, None, "You haven't created any chatrooms!")

                    else: 
                        self._message(bob, None,"That's not a valid command! Refreshing menu...")
            
            except Exception as e:
                print("Exception in _listen:", repr(e))
                traceback.print_exc() 
                endRoom = self._leave(bob, True)
                self._message(bob, endRoom, "i go bye bye now")
                break 

    
  
    def _menu(self, bob: currentClient):

        # Ask the user for their choice
        self._message(bob, None,"What would you like to do?")
            
        # (1) Join
        self._message(bob, None, "(1) Join an existing chat room")
        self._message(bob, None,"     *To join enter: 1 <name_of_room_to_join>")
        counter = 0

        # CRITICAL SECTION
        with self._lock:
            # list all avalible rooms
            print(f"listing chat rooms") # debug
            self._message(bob, None, "Existing chatrooms:")
            for chat in self._chatrooms:
                print(f"{chat.getRoomName()}: {chat.getUsers()}") # debug
                # remove this chatroom, if there are no users in it
                if chat.getUsers() < 1:
                    self._chatrooms.remove(chat)
                else:
                    toPrint = "    " + chat.getRoomName()
                    self._message(bob, None, toPrint)
                    counter += 1

        if counter < 1:
            self._message(bob, None, "     Nothing here!")

        self._message(bob, None, "To exit a chatroom you are within, enter: i go bye bye now")

        # (2) Create
        self._message(bob, None,"(2) Create a new chat room")
        self._message(bob, None, "    *To create enter: 2 <name_of_your_new_chatroom>")

        # (3) Leave
        self._message(bob, None,"(3) Leave the server")
        
        # (4) List
        self._message(bob, None, "(4) List members in an existing chatroom")
        self._message(bob, None, "     *To list chatroom members enter: 4 <name_of_chatroom>")

        # (5) Delete 
        # Only display this option, if the client has created any chatrooms
        if bob.getCreated():
            self._message(bob, None,"(5) Delete your own chat room")
            # print all bob's created chatrooms 
            # this is not critical, because no one except bob, will alter the list bob._created
            for chat in bob.getCreated():
                self._message(bob, None, chat)
            self._message(bob, None,"     *To delete one of your chatrooms, enter: 5 <chatroom_to_delete>")

                 
    # Desc:
    # Input:
    # Return: 
    def _join(self, bob: currentClient, toJoin: str):

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
    def _create(self, bob: currentClient, toCreate: chatroom):
        
        print(f"toCreate = {toCreate}") # debug

        # CRITICAL SECTION
        with self._lock:
            for chat in self._chatrooms:
                print(f"{chat}") # debug
                if chat.getRoomName() == toCreate.getRoomName():
                    return False
                     
        bob.setInroom(toCreate)
        bob.addCreated(toCreate.getRoomName())
        # CRITICAL SECTION 
        with self._lock:
            self._chatrooms.append(toCreate)

            # might need to remove this debugging inside a lock 
            print(f"chatrooms after append:") # debug
            for chat in self._chatrooms: # debug
                print(f"{chat.getRoomName()}") # debug
 
        return True
    
    # Desc:
    # Input:
    # Return: 
    def _leave(self, bob: currentClient, gone: bool):
        print(f"client {bob} is leaving") # debug
        # NO MESSAGING SHOULD BE CALLED FROM LEAVE, prevent deadlock 
        
        # we can return this, and if in a good place in the code
        # we send a message AFTER LEAVE to bob's chatroom 
        room = bob.getInroom() 

        # CRITICAL SECTION
        with self._lock:
            for chat in self._chatrooms:
                if chat == bob._inroom:
                    chat.decrement()
                    break 
        bob.setInroom(None)
     
        if gone:
            bob.getClientSocket().close()
            # CRITICAL SECTION 
            with self._lock:
                for user in self._activeClients:
                    if user == bob:
                        self._activeClients.remove(user)
                        break  

        return room
 
       
       
    # Desc:
    # Input:
    # Return: 
    def _list(self, bob: currentClient, toList: str):

        count = 0

        self._message(bob, None, f"Users in {toList}:")
        
        # CRITICAL SECTION
        with self._lock:
            # list members in chatroom toList
            for user in self._activeClients:
                print(f"{user.getUsername()}: {user.getInroom()}") # debug
                if user.getInroom():
                    if user.getInroom().getRoomName() == toList:
                        count += 1
                        message = "    " + user.getUsername()
                        self._message(bob, None, message)

        print(f"count1 = {count}")
        if count < 1:
            self._message(bob, None, f"It looks like {toList} doesn't exist anymore!")

        print("Returning from list") # debug
        

    # Desc:
    # Input:
    # Return:  
    def _delete(self, bob: currentClient, toDelete: str):

        # CRITICAL SECTION
        with self._lock:
            for chat in self._chatrooms:
                if chat:
                    if chat.getRoomName() == toDelete:
                        deleteRoom = chat
                        self._chatrooms.remove(chat)
                        break 

        self._message(bob, chat, "Sorry eveybody i end room now bye")

        # CRITICAL SECTION
        with self._lock:
            for user in self._activeClients:
                if user.getInroom():
                    if user.getInroom().getRoomName() == toDelete:
                        user.setInroom(None)

        bob.removeCreated(toDelete)

 
    
    # Desc:
    # Input:
    # Return: 
    def _message(self, bob: currentClient, room: chatroom, message: str):

        # if bob is not in a room, the message is from the server to bob
        if room == None:
            recipients = []
            recipients.append(bob)
            formatMessage = message 
            print(f"formatMessage = {formatMessage}") # debug

        else:
            formatMessage = bob.getUsername() + " ~ " + message
            print(f"formatMessage = {formatMessage}") # debug

            # CRITICAL SECTION
            with self._lock:
                print(f"getting recipients") # debug
                recipients = [u for u in self._activeClients if u.getInroom() == room]

        print(f"{recipients}") # debug
        # Don't lock message sending!
        for user in recipients:
            print(f"sending to {user.getUsername()}") # debug
            try:
                user.getClientSocket().sendall(formatMessage.encode())
            # call leave handler 
            except ConnectionResetError:
                print(f"removing deleted client {user.getUsername()}") # debug
                self._leave(user, True)


 
# currentClient object class 
class currentClient:


    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def __init__(self, newClientSocket, newUsername: str, newInroom: chatroom):
        self._clientSocket = newClientSocket
        self._username = newUsername
        self._created = []
        self._inroom = newInroom

    # setters and getters

    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def setInroom(self, newInroom: chatroom):
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
    def setUsername(self, newUsername:str):
        self._username = newUsername

    # Desc: Constructor with parameters
    # Input: 
    # Return: None  
    def getUsername(self):
        return self._username

    
    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def addCreated(self, newRoomName: str):
        self._created.append(newRoomName)

    
    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def removeCreated(self, delRoomName: str):
        self._created.remove(delRoomName)

class chatroom:

    # Desc: Constructor with parameters
    # Input: 
    # Return: None
    def __init__(self, newRoomName: str, users: int):
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
    global HOST
    global PORT
    
    HOST = input("Enter host on which to run server: ")
    PORT = int(input ("Enter port on which to run server: "))

    
    try:
        myServer = serverManagment(HOST, PORT)
    except:
        print("An error occured!")
        exit(0)
     

if __name__=='__main__':
    main()
# means main only runs when script is run directly 
# main will NOT run when script is imported as a module 