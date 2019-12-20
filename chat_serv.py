import socket
import select #os level i/o without protablity issue with differet os

HEADER_LENGTH=10
IP="127.0.0.1"
PORT=1234

server_socket =socket.socket(socket.AF_INET,socket.SOCK_STREAM)


server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind((IP,PORT))

server_socket.listen()
sockets_list=[server_socket]
#all the clients socket  will be stored in that list socket_list
clients={}
#clients socket  and the message recieved from them will be stored as key value pair
def receive_message(client_socket):
    try:
        message_header=client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length=int(message_header.decode("utf-8").strip(" "))
        #message_length contains the lenght of message the server is going to receive 
        #str.strip([chars]) is used to remove the char(passed as parameters)
        #from the sring
        return {"header":message_header,"data":client_socket.recv(message_length)}
    except:
        return False

    
    
while True:
    read_sockets, write_sockets, exception_sockets=select.select(sockets_list,[],sockets_list)
    #1st parameter contains list of sockets ready for reading 
    #2nd paramets ....................................writing
    #3..............................sockets with some exception
    #returns a subset (tuple) of all the three list passed as parameters
    for socks in read_sockets:
        if socks == server_socket:
            #means client sent a connectionREQ to the server, and were going to receive the from server_socket
            client_socket,client_address = server_socket.accept()
            #now thw connection is established we can receive the message from client side
            user=receive_message(client_socket)
            #user={"header":message_header(size of message),"data":actual message of length specifed in header}
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket]=user
            #receive_message returns false when some connection error occus
            #when client disconnects
            print(f"accepted new connection from {client_address} data:{user['data'].decode('utf-8')}")
        else:
            message=receive_message(socks)
            if message is False:
                print(f"closet connection from{clients[socks]['data'].decode('utf-8')}")
                sockets_list.remove(socks)
                del clients[socks]
                continue
            user=clients[socks]
            print(f"recieved message from{user['data'].decode('utf-8')}:{message['data'].decode('utf-8')}")
            for client_sock in clients:
                if client_sock!= socks:
                    client_sock.send(user['header']+user['data']+message['header']+message['data'])
    for socks in exception_sockets  :
         sockets_list.remove(socks)
         del clients[socks]
