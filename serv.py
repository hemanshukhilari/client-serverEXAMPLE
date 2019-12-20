import socket
import  time
import pickle

 
HEADERSIZE=10

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.bind((socket.gethostname(),1234))
s.listen(5)

while True:
    clientsocket, adrss= s.accept()
    print(f"connected {adrss}{clientsocket}")

    d={1:"hello",2:"slut"}
    msg=pickle.dumps(d)#binary string

    msg=bytes(f"{len(msg):<{HEADERSIZE}}","utf-8")+msg
    clientsocket.send(msg)
    
    '''msg="welcomwe to server"
    msg=f"{len(msg):<{HEADERSIZE}}"+msg
    #OP->18      welcomwe to server 
    clientsocket.send(bytes(msg,"utf-8"))
    
    while True:
        time.sleep(3)
        msg=f"the timme is {time.time()}"
        msg=f"{len(msg):<{HEADERSIZE}}"+msg
        clientsocket.send(bytes(msg,"utf-8"))'''
    
