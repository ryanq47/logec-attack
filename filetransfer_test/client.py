#https://stackoverflow.com/questions/27241804/sending-a-file-over-tcp-sockets-in-python
import socket               # Import socket module
import os
import math

s = socket.socket()         # Create a socket object
host = "127.0.0.1" # Get local machine name
port = 5000               # Reserve a port for your service.

s.connect((host, port))
#s.send("Hello server!")
f = open('data.txt','rb')
size = os.path.getsize('data.txt')

number_of_it =  math.ceil(size / 1024)

print(size)

print(number_of_it)

print('Sending...')



for i in range(1, number_of_it + 1): # sending interations + 1 to get all data

    #while (l):
    print('Sending...')
    data = f.read(1024)
    l = data
    s.send(l)
    

f.close()
print("Done Sending")

s.shutdown(socket.SHUT_WR)
print("End of script")
s.close 