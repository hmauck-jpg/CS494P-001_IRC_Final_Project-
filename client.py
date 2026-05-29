

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
import traceback 
 

HOST = '127.0.0.1'
PORT = 4000
SHUTDOWN = False


# implement ncurses (maybe later use Vue)
# replaces print and input

# add an option to manually change host and port, so grader can run it on whatever works
      
# Desc: Listens for messages from the server
# Input: Client socket connected to the server
# Return: Void
def listenServer(client, chatwin):
    global SHUTDOWN
    while not SHUTDOWN:
        try:
            message = client.recv(2048).decode('utf-8') 
            # throws exception if client is already closed 
            if not message:
                SHUTDOWN = True
                # End messages need to linger in the terminal after the main thread ends
                print("\nServer closed the connection\n")
                break 
            
            # just directly print whatever the server sends, it should be 
            # formatted as intended 
            try:
                chatwin.addstr("\n" + message)
                chatwin.refresh()
            except:
                pass
       
        except Exception:
            if not SHUTDOWN:
                # End messages need to linger in the terminal after the main thread ends
                print("\nDisconnected from server.\n")
            SHUTDOWN = True
            break


# Desc:  
# Input: 
# Return: 
def messageServer(client, inputwin):
    global SHUTDOWN 
    curses.echo()

    while not SHUTDOWN:
        try:
            inputwin.clear()
            inputwin.addstr("> ")
            inputwin.refresh()
            # Get message from input, encode and send the message to the server
            message = inputwin.getstr().decode('utf-8')
            # throws error when main thread exits 
            if message:
                client.sendall(message.encode())
                # throws an exception if client is closed
            else:
                pass
        except (KeyboardInterrupt, EOFError):
            SHUTDOWN = True
            break
     
  


def cursesMain(stdscr):
    global SHUTDOWN

# will this handle ctrl c
    import signal
    def handle_sigint(sig, frame):
        global SHUTDOWN
        SHUTDOWN = True
    signal.signal(signal.SIGINT, handle_sigint)

    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # Create windows
    max_y, max_x = stdscr.getmaxyx()
    chatwin = curses.newwin(max_y - 3, max_x, 0, 0)
    chatwin.scrollok(True)
    inputwin = curses.newwin(3, max_x, max_y - 3, 0)
    inputwin.scrollok(True)


    # create socket object 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    try:
        client.connect((HOST, PORT))
        chatwin.addstr("Successfully connected to server\n")
        chatwin.refresh()
    except:
        return 0

    # Start threads
    threading.Thread(target=listenServer, args=(client, chatwin), daemon=True).start()
    threading.Thread(target=messageServer, args=(client, inputwin), daemon=True).start()
 
    try:
        while not SHUTDOWN:
            time.sleep(0.1)
    except KeyboardInterrupt:
        SHUTDOWN = True

    client.close()
    return 1


def main():
    global HOST
    global PORT 

    HOST = input("Enter host the client is connecting to: ")
    try:
        PORT = int(input("Enter port the client is connecting to: "))

        if curses.wrapper(cursesMain) < 1:
            print(f"Unable to connect to server {HOST}, {PORT}\n")

    except ValueError:
        print("That's not a valid input for the port!\n")
    except Exception as e:
        print("Error occured in curses: ", repr(e))
        traceback.print_exc() 

    
    
    print("\nThank you for stopping by!\n")
    
if __name__=='__main__':
    main()

   