import socket
import pickle

HEADERSIZE=10
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.connect((socket.gethostname(),1234))

while True:
    full_msg=b""
    new_msg=True
    while True:
        msg= s.recv(16)#msg is a binary string
        if new_msg:
            print(f"new msg len:{msg[:HEADERSIZE]}")
            msglen=int(msg[:HEADERSIZE])
            #msg[:HEADRERSIZE] will contain the first 10 charcters of msg since HEADERSIZE=10 
            #msglen will contain the length of the msg recieved,since the lenth is int the first 10 characters of the msg itself 
            new_msg=False
            
        full_msg+=msg
        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recieved")
            print(full_msg[HEADERSIZE:])
            d=pickle.loads(full_msg[HEADERSIZE:])
            print(d)
            new_msg=True
            full_msg=b""
print(x)
#print(socket.gethostbyname(socket.gethostname()))
