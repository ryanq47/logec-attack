## Exploit client

import socket

PORT = 5058
HEADER = 64

DISCONNECT_MESSAGE = "!quit"
FORMAT = 'utf-8'
SERVER = "192.168.0.52"

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    ## first message sent
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    recieved_message = client.recv(10000)

    ## making sure you don't see your own messages
    #if SERVER in str(recieved_message):
        #pass
    print(recieved_message.decode(FORMAT))

## changing it up to a (sort of) real chatbot

def mainloop():
    user_input = input("|ChatBot: ")
    send(user_input)


if __name__ == "__main__":
    ## sending initial message (should be random in future iterations)
    send(" ")

    while True:
        mainloop()

send(DISCONNECT_MESSAGE)