import socket

s = socket.socket()
host = "0.0.0.0"
port = 5000

s.bind((host,port))

with open('data_exfil.txt','wb') as f:
    s.listen(5)
    print("listening")

    while True:
        
        c, addr = s.accept()
        print("got connection from", addr)
        print("getting data")

        ## receiving inital bit
        l = c.recv(1024)
        #print(f"{l} << should be data here")

        ## while there is data being transfered, write to  file
        while (l):
            print(l)
            f.write(l)
            l =  c.recv(1024)

        print("done")
        c.close()
        #exit()