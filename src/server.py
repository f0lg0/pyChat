import socket
import select
import sys

HEADER_LENGTH = 10

IP = "192.168.1.34"
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket object with socket families types --> streaming socket
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

server.bind((IP, PORT))
server.listen(10)

print(f"Starting server ({IP}) on port {PORT}")


sockets_list = [] # sockets list

def receiveMsg():     
    print("Receiving...")
    msg = client_socket.recv(2048) 

    if msg != "": 
        # print message details
        print("<" + address[0] + "> " + msg.decode("utf-8"))
    else:
        print("Empty")


while True:
    client_socket, address = server.accept()
    print(f"Connection from {address} has been established!")
    sockets_list.append(client_socket)
    client_socket.send(bytes("Welcome to Folgo's Basement!", "utf-8"))

    if sockets_list.__len__() > 1:
        receiveMsg()