import socket
import pickle
import threading
import sys
import argparse
import os
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Message:
    shost: str
    dhost: str
    username: str
    date: str
    cont: bytes
    size: int
    typ: str

    def pack(self):
        return pickle.dumps(self)

class Server:
    def __init__(self, ip, port, buffer_size):
        self.IP = ip
        self.PORT = port
        self.BUFFER_SIZE = buffer_size

        self.USERNAME = "server"

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
            users.write(data.decode("utf-8") + '\n')

    def logChat(self, data):
        timestamp = datetime.now()
        with open(self.chat_log, "a", encoding = "utf-8") as chatlog:
            chatlog.write(data.decode("utf-8") + " " + str(timestamp) + '\n')

    def current(self, data):
        """ wasn't sure about using with here """
        self.currentchat = open(self.current_chat, "a+", encoding = "utf-8")
        self.currentchat.write(data.decode("utf-8") + '\n')

    def checkUsername(self, client_socket, address, data):
        flag = False

        for user in self.database:
            if self.database[user] == data.cont.decode("utf-8"):
                flag = True
                self.temp_f = True

                content = b"[*] Username already in use!"
                warning = Message(self.IP, address, self.USERNAME, str(datetime.now()), content, len(content), 'username_taken')

                client_socket.send(warning.pack())
                break

        if flag == False:
            self.database.update( {address : data.cont.decode("utf-8")} )
            self.logUsers(data.cont)

            content = b"[*] You have joined the chat"
            joined = Message(self.IP, address, self.USERNAME, str(datetime.now()), content, len(content), 'approved_conn')
            client_socket.send(joined.pack())

        print(self.database)

    def exportChat(self, client_socket, address):
        with open(self.current_chat, "rb") as chat:
            content = chat.read()

            packet = Message(self.IP, address, self.USERNAME, str(datetime.now()), content, len(content), 'export')

            for connection in self.connections:
                if connection == client_socket:
                    connection.send(packet.pack())
                    print("[*] Sent!")



    def commandList(self, client_socket):
        cdict = pickle.dumps(self.command_list)
        for connection in self.connections:
            if connection == client_socket:
                connection.send(cdict)
                print("[*] Sent!")

    def handler(self, client_socket, address):
        while True:
            data = client_socket.recv(self.BUFFER_SIZE)
            if not data:
                print(f"[*] {address} disconnected")
                disconnected_msg = bytes(f"[*] {self.database.get(address)} has left the chat", "utf-8")

                left_msg_obj = Message(self.IP, "allhosts", self.USERNAME, str(datetime.now), disconnected_msg, len(disconnected_msg), 'default')
                left_msg = left_msg_obj.pack()

                for connection in self.connections:
                    connection.send(left_msg)

                self.connections.remove(client_socket)

                if not self.connections:
                    os.remove(self.current_chat)

                del self.database[address]
                client_socket.close()
                break

            loaded = pickle.loads(data)

            if loaded.typ == 'setuser':
                self.checkUsername(client_socket, address, loaded)

                if self.temp_f == True:
                    continue
            else:
                if loaded.cont != b'':
                    if loaded.typ == 'default':
                        self.logChat(loaded.cont)
                        self.current(loaded.cont)
                    else:
                        self.logChat(loaded.cont)

                    if loaded.typ == 'export':
                        print("*** Sending chat...")
                        self.exportChat(client_socket, address)
                    elif loaded.typ == 'help':
                        print("*** Sending command list...")
                        self.commandList(client_socket)
                    else:
                        for connection in self.connections:
                            if connection != client_socket:
                                connection.send(data)


    def acceptConnections(self):
        while True:
            client_socket, address = self.server.accept()
            print(f"[*] Connection from {address} has been established!")
            self.logConnections(address[0])

            cThread = threading.Thread(target = self.handler, args = (client_socket, address))
            cThread.daemon = True
            cThread.start()

            self.connections.append(client_socket)


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", dest = "port", help = "Start server on port X")

    options = parser.parse_args()

    if not options.port:
        # parser.error("*** Please specify a port to bind connections ***")
        # raise argparse.ArgumentError(options.port, "") -> we can also use this but I don't know if it is great
        raise Exception # just raising a normal exception if we don't get values
    else:
        return options

def main():
    try:
        options = getArgs()
        PORT = int(options.port)
    except Exception: # if the user doesn't parse values from the command line
        PORT = int(input("*** Start server on port > "))

    HOSTNAME = socket.gethostname()
    IP =  socket.gethostbyname(HOSTNAME)
    BUFFER_SIZE = 1024

    server = Server(IP, PORT, BUFFER_SIZE)

    try:
        server.startServer()
        server.acceptConnections()

    except Exception as e:
        print("General error", str(e))

if __name__ == "__main__":
	main()
