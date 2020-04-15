import socket
import pickle
import threading
import sys
import argparse
import os
from datetime import datetime
from message import Message
from streaming import createMsg, streamData

from Crypto.Cipher import PKCS1_OAEP # RSA based cipher using Optimal Asymmetric Encryption Padding
from Crypto.PublicKey import RSA #  to generate the keys

class RSAEncryption:
    def __init__(self, bits):
        self.BITS = bits

    def generatePrivateKey(self):
        self.private_key = RSA.generate(self.BITS)

    def generatePublicKey(self):
        self.public_key = self.private_key.publickey()

    def writeToFile(self):
        private_pem = self.private_key.exportKey().decode("utf-8")
        public_pem = self.public_key.exportKey().decode("utf-8")

        with open('./keys/private.pem', 'w+') as private:
            private.write(private_pem)
        
        with open('./keys/public.pem', 'w+') as private:
            private.write(public_pem)

    def importKeys(self):
        keys = []
        pr_key = RSA.importKey(open('./keys/public.pem', 'r').read())
        pu_key = RSA.importKey(open('./keys/public.pem', 'r').read())

        keys.append(pr_key)
        keys.append(pu_key)

        return keys


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

        # # encryption
        # self.enc = RSAEncryption(1024)

        # self.enc.generatePrivateKey()
        # self.enc.generatePublicKey()
        # self.enc.writeToFile()
        # self.keys = self.enc.importKeys()

        # self.cipher = PKCS1_OAEP.new(key = self.keys[0])

    def startServer(self):
        try:
            self.server.bind((self.IP, self.PORT))
        except socket.error as e:
            print(str(e))

        self.server.listen(10)

        '''
        #Load in previously created usernames
        try:
            usersFile = open("./logs/users.txt", "r")
        except IOError as e:
            print(str(e))
        
        users = usersFile.readlines()
        
        #loop through file, and no including empty lines, strip the line break escape char and add username to database
        for user in users[1:]:
            if(user != "\n"):
                self.database.update({"offline": user.replace("\n", "")})  
        #just print out the usernames line by line

        print(f"pre-existing users: ")
        for account in self.database.values():
            if(account != "username"):
                print(account)

        '''
    
        print(f"[*] Starting server ({self.IP}) on port {self.PORT}")

    def acceptConnections(self):
        while True:
            client_socket, address = self.server.accept()
            print(f"[*] Connection from {address} has been established!")
            self.logConnections(address[0])

            cThread = threading.Thread(target = self.handler, args = (client_socket, address))
            cThread.daemon = True
            cThread.start()

            self.connections.append(client_socket)
            # self.sharePubKey(client_socket)

    # def sharePubKey(self, client_socket):
    #     with open("./keys/public.pem", 'rb') as f:
    #         key = createMsg(pickle.dumps(f.read()))
    #         client_socket.send(key)
    #     print("*** Public Key sent ***")

    def logConnections(self, address):
        contime = datetime.now()
        with open(self.cons_log, "a") as cons:
            cons.write(address + ">" + str(contime) + '\n')

    def logUsers(self, data):
        with open(self.users_log, "a", encoding = "utf-8") as users:
            users.write(data + '\n')

    def logChat(self, data):
        decoded_data = data.decode("utf-8")
        timestamp = datetime.now()
        with open(self.chat_log, "a", encoding = "utf-8") as chatlog:
            chatlog.write(decoded_data + " " + str(timestamp) + '\n')

    def current(self, data):
        decoded_data = data.decode("utf-8")
        """ wasn't sure about using with here """
        self.currentchat = open(self.current_chat, "a+", encoding = "utf-8")
        self.currentchat.write(decoded_data + '\n')

    def checkUsername(self, client_socket, address, data):
        flag = False
        decoded_content = data.cont.decode("utf-8")
        # decrypted_data = self.cipher.decrypt(data).decode("utf-8")

        for user in self.database:
            if self.database[user] == decoded_content:
                flag = True
                self.temp_f = True

                content = "[*] Username already in use!"
                # encrypted_content = self.cipher.encrypt(content)

                warning = Message(self.IP, address, self.USERNAME, str(datetime.now()), content, 'username_taken')

                client_socket.send(warning.pack())
                break

        if flag == False:
            self.database.update( {address : decoded_content} )
            self.logUsers(decoded_content)

            content = "[*] You have joined the chat!"
            # encrypted_content = self.cipher.encrypt(content)

            joined = Message(self.IP, address, self.USERNAME, str(datetime.now()), content, 'approved_conn')
            client_socket.send(joined.pack())

    def exportChat(self, client_socket, address):
        with open(self.current_chat, "rb") as chat:
            content = chat.read()

            packet = Message(self.IP, address, self.USERNAME, str(datetime.now()), content, 'export')

            for connection in self.connections:
                if connection == client_socket:
                    connection.send(packet.pack())
                    print("[*] Sent!")


    def commandList(self, client_socket):
        cdict = createMsg(pickle.dumps(self.command_list)) # manually crafting since i can't call pack() -> not a message obj
        for connection in self.connections:
            if connection == client_socket:
                connection.send(cdict)
                print("[*] Sent!")

    def closeConnection(self, client_socket, address):
        disconnected_msg = bytes(f"[{address[0]}] has left the chat", "utf-8")
        left_msg_obj = Message(self.IP, "allhosts", self.USERNAME, str(datetime.now), disconnected_msg, 'default')
        left_msg = left_msg_obj.pack()

        self.connections.remove(client_socket)

        for connection in self.connections:
            connection.send(left_msg)

        if not self.connections:
            try:
                os.remove(self.current_chat)
            except FileNotFoundError:
                print("*** Nothing to clear in the logs")

        try:
            del self.database[address]
        except KeyError:
            pass
        client_socket.close()

    def handler(self, client_socket, address):
        while True:
            try:
                data = streamData(client_socket)
            except ConnectionResetError:
                print(f"*** [{address[0]}] unexpectedly closed the connetion, received only an RST packet.")
                self.closeConnection(client_socket, address)
                break

            if not data:
                print(f"*** [{address[0]}] disconnected")
                self.closeConnection(client_socket, address)
                break

            if data.typ == 'setuser':
                self.checkUsername(client_socket, address, data)

                if self.temp_f == True:
                    continue
            else:
                if data.cont != b'':
                    if data.typ == 'default':
                        self.logChat(data.cont)
                        self.current(data.cont)
                    else:
                        self.logChat(data.cont)

                    if data.typ == 'export':
                        print("*** Sending chat...")
                        self.exportChat(client_socket, address)
                    elif data.typ == 'help':
                        print("*** Sending command list...")
                        self.commandList(client_socket)
                    else:
                        for connection in self.connections:
                            if connection != client_socket:
                                connection.send(data.pack())



def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", dest = "port", help = "Start server on port X")

    options = parser.parse_args()

    if not options.port:
        raise Exception
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
