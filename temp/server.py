import socket
import pickle
import threading
import sys
from datetime import datetime
from msgManager import createMsg
from msgManager import streamData

HEADERSIZE = 10

class Server:
    def __init__(self, ip, port, buffer_size):
        self.IP = ip
        self.PORT = port
        self.BUFFER_SIZE = buffer_size

        self.temp_f = False

        self.connections = []
        self.database = {
            "host" : "username"
        }

        self.command_list = {
            "[export_chat]" : "export current chat",
            "[help]" : "display possibile commands"
        }

        self.users_log = "./logs/users.txt"
        self.chat_log = "./logs/chatlog.txt"
        self.cons_log = "./logs/cons.txt"
        self.current_chat = "./logs/currentchat.txt"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def startServer(self):
        try:
            self.server.bind((self.IP, self.PORT))
        except socket.error as e:
            print(str(e))

        self.server.listen(10)

        print(f"[*] Starting server ({self.IP}) on port {self.PORT}")

    def logConnections(self, address):
        contime = datetime.now()
        with open(self.cons_log, "a") as cons:
            cons.write(address + ">" + str(contime) + '\n')

    def logUsers(self, data):
        with open(self.users_log, "a", encoding = "utf-8") as users:
            users.write(data + '\n')

    def logChat(self, data):
        timestamp = datetime.now()
        with open(self.chat_log, "a", encoding = "utf-8") as chatlog:
            chatlog.write(data + " " + str(timestamp) + '\n')

    def current(self, data):
        """ wasn't sure about using with here """
        self.currentchat = open(self.current_chat, "a", encoding = "utf-8")
        self.currentchat.write(data + '\n')

    def checkUsername(self, client_socket, address, data):
        flag = False
        decoded_user = data

        for user in self.database:
            if self.database[user] == decoded_user:
                flag = True
                self.temp_f = True
                warning = "[*] Username already in use!"
                client_socket.send(warning.encode("utf-8"))
                break

        if flag == False:
            self.database.update( {address : decoded_user} )
            self.logUsers(decoded_user)
            client_socket.send(createMsg("[*] You have joined the chat!"))

        print(self.database)

    def exportChat(self, client_socket):
        with open(self.current_chat, "r", encoding = "utf-8") as chat:
            data = chat.read()

            for connection in self.connections:
                if connection == client_socket:
                    connection.send(createMsg(data))
                    print("[*] Sent!")


    #sends command list to the specified 'client_socket'
    def commandList(self, client_socket):
        cdict = pickle.dumps(self.command_list)
        for connection in self.connections:
            if connection == client_socket:
                connection.send(cdict)
                print("[*] Sent!")

    def handler(self, client_socket, address):
        while True:    
            #streams the data in
            #side note: the buffer size needs to be limited by the headersize as the first data chunk streamed will be the length to expect
            decoded_data = streamData(client_socket, HEADERSIZE)

            print("Received:", decoded_data)

            if decoded_data[0:5] == "[usr]":
                self.checkUsername(client_socket, address, decoded_data)

                if self.temp_f == True:
                    continue

            else:
                #I restructure this to be a bit more efficient
                if decoded_data != b'':
                    if "[export_chat]" in decoded_data:
                        print("[*] Sending chat...")
                        self.exportChat(client_socket)
                        self.logChat(decoded_data)
                    else:
                        self.logChat(decoded_data)
                        self.current(decoded_data)
                
                if "[help]" in decoded_data:
                    print("[*] Sending command list...")
                    self.commandList(client_socket)
                else:
                    for connection in self.connections:
                        if connection != client_socket:
                            connection.send(bytes(decoded_data, "utf-8"))

                if not decoded_data:
                    print(f"[*] {address} disconnected")

                    left_msg = bytes(f"[*] {self.database.get(address)} has left the chat", "utf-8")
                    for connection in self.connections:
                        connection.send(left_msg)

                    self.connections.remove(client_socket)

                    if not self.connections:
                        self.currentchat.truncate(0)

                    del self.database[address]
                    client_socket.close()
                    break



    def acceptConnections(self):
        while True:
            client_socket, address = self.server.accept()
            print(f"[*] Connection from {address} has been established!")
            self.logConnections(address[0])

            cThread = threading.Thread(target = self.handler, args = (client_socket, address))
            cThread.daemon = True
            cThread.start()

            self.connections.append(client_socket)


def main():
    HOSTNAME = socket.gethostname()
    IP =  socket.gethostbyname(HOSTNAME)
    PORT = int(input("[*] Start server on port> "))
    BUFFER_SIZE = 10

    server = Server(IP, PORT, BUFFER_SIZE)

    try:
        server.startServer()
        server.acceptConnections()

    except Exception as e:
        print("General error", str(e))

if __name__ == "__main__":
	main()
