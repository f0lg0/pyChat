import socket
import json
import threading
import sys
import argparse
import os
from datetime import datetime
from message import Message
from streaming import createMsg, streamData, initializeAES, decryptMsg
from clientConnectionObj import ClientConnection
import pyDHE
import time

serverDH = pyDHE.new() # DiffieHellman object

class Server:
    def __init__(self, ip, port, buffer_size):
        self.IP = ip
        self.PORT = port
        self.BUFFER_SIZE = buffer_size

        self.USERNAME = "*server*"

        self.temp_f = False # flag for loop logic

        # holds all the socket objects
        #FLAGGED
        self.connections = []

        #contains the ip associated with username
        #FLAGGED
        self.database = {
            "host" : "username"
        }

        # holds all the client enc keys associated with IPs
        #FLAGGED
        self.keyList = {
            "client" : "key"
        }

        # holds a list of client connection objects (eventully we should have just this)
        self.clientConnections = []

        self.command_list = {
            "[export_chat]" : "export current chat",
            "[help]" : "display possibile commands"
        }
        

        self.users_log = "./logs/users.txt"
        self.chat_log = "./logs/chatlog.txt"
        self.cons_log = "./logs/cons.txt"
        self.current_chat = "./logs/currentchat.txt"

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def startServer(self):
        try:
            self.server.bind((self.IP, self.PORT))
        except socket.error as e:
            print(str(e))

        self.server.listen(10)

        print(f"[*] Starting server ({self.IP}) on port {self.PORT}")

    def acceptConnections(self):
        while True:
            client_socket, address = self.server.accept()
            print(f"[*] Connection from {address} has been established!")
            self.logConnections(address[0])

            # instantiate a client connection obj with the username and encrytion key initially set to null
            self.clientConnections.append(ClientConnection(client_socket, None, None))

            cThread = threading.Thread(target = self.handler, args = [self.findConnectionFromSocket(client_socket)])
            cThread.daemon = True
            cThread.start()

    
            self.connections.append(client_socket)
            self.shareVector(client_socket, address[0])
            self.sharePublicKey(client_socket, address[0])
            time.sleep(0.1) # to avoid buffer congestion
           
    def stopServer(self):
        for conn in self.connections:
            conn.close()

        self.server.close()

    def shareVector(self, client_socket, address):
        with open('./vector', 'rb') as vector:
            content = vector.read().decode("utf-8")
            packet = Message(self.IP, address, self.USERNAME, str(datetime.now()), content, 'iv_exc')
            client_socket.send(packet.pack())


    def sharePublicKey(self, client_socket, address):
        packet  = Message(self.IP, address, self.USERNAME, str(datetime.now()), str(serverDH.getPublicKey()), 'key_exc')
        client_socket.send(packet.pack())

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
        """ wasn't sure about using 'with' here """

        self.currentchat = open(self.current_chat, "a+", encoding = "utf-8")
        self.currentchat.write(data + '\n')

    def checkUsername(self, client_socketObj, data):
        flag = False

        for user in self.database:
            if self.database[user] == data.cont:
                flag = True
                self.temp_f = True

                content = "[*] Username already in use!"

                warning = Message(self.IP, client_socketObj.getIP(), self.USERNAME, str(datetime.now()), content, 'username_taken')

                self.sendMessageToClient(client_socketObj, warning)
                break

        if flag == False:
            self.database.update( {client_socketObj.getIP() : data.cont} )
            client_socketObj.username = data.cont

            # self.logUsers(decoded_content)

            content = "[*] You have joined the chat!"

            joined = Message(self.IP, client_socketObj.getIP(), self.USERNAME, str(datetime.now()), content, 'approved_conn')
            self.sendMessageToClient(client_socketObj, joined)

    def exportChat(self, client_socketObj):
        with open(self.current_chat, "rb") as chat:
            content = chat.read().decode("utf-8")

            packet = Message(self.IP, client_socketObj.getIP(), self.USERNAME, str(datetime.now()), content, 'export')

            self.sendMessageToClient(client_socketObj, packet)
            print("[*] Sent!")
                    

    def sendCommandList(self, client_socketObj):
        packet = Message(self.IP, client_socketObj.getIP(), self.USERNAME, str(datetime.now()), self.command_list, 'help', True)
        
        self.sendMessageToClient(client_socketObj, packet)
        print("[*] Sent!")
                

    def closeConnection(self, client_socketObj):
        disconnected_msg = f"[{client_socketObj.username}] has left the chat"
        left_msg_obj = Message(self.IP, "allhosts", self.USERNAME, str(datetime.now()), disconnected_msg, 'default')

        self.connections.remove(client_socketObj.socketObj) # FLAGGED
        self.clientConnections.remove(client_socketObj)

        for connection in self.clientConnections:
            self.sendMessageToClient(connection, left_msg_obj)

        if not self.clientConnections:
            try:
                os.remove(self.current_chat)
            except FileNotFoundError:
                print("*** Nothing to clear in the logs")

        try:
            del self.database[client_socketObj.getIP()]
        except KeyError:
            pass

        client_socketObj.socketObj.close()

    '''
        @ will send a message (content) to a specified 'client' using their unique encryption key
        Preconditions:
            * the content parameter has to be a message object (unpacked)
            * client has to be a socket connection object (special object containing sock obj, key and username)
    '''
    def sendMessageToClient(self, client, content):
        key = client.encKey 
        initializeAES(str(key).encode("utf-8")) # update the servers encryption class with the specific clients key
        client.socketObj.send(content.pack()) # send the message with the new AES object initialized
  
    def handler(self, client_socketObj):
        client_socket = client_socketObj.socketObj # renaming 
        address = client_socketObj.getIP() # renaming

        while True:
            try:
                ''' HANDLING DATA FLOW '''
                data = streamData(client_socket) # stream it
                data = decryptMsg(data, client_socketObj.encKey) # decrypting it
                data = Message.from_json(data) # converting to obj
                
            except ConnectionResetError:
                print(f"*** [{address}] unexpectedly closed the connetion, received only an RST packet.")
                self.closeConnection(client_socketObj)
                break
            except AttributeError:
                print(f"*** [{address}] disconnected")
                self.closeConnection(client_socketObj)
                break
            except UnicodeDecodeError:
                print(f"*** [{address}] disconnected due to an encoding error")
                self.closeConnection(client_socketObj)
                break
            except TypeError:
                print(f"*** [{address}] disconnected")
                self.closeConnection(client_socketObj)
                break
            
            if data.typ == 'setuser':
                # clientConnection obj updated in the self.checkUsername function
                self.checkUsername(client_socketObj, data)
                
                if self.temp_f == True:
                    continue
            elif data.typ == 'key_exc':
                finalKey = serverDH.update(int(data.cont)) # generating the shared private secret 
                self.keyList.update( { address : finalKey }) # adding it to database FLAGGED
                client_socketObj.encKey = finalKey
            else:
                if data.cont != '':
                    if data.typ == 'default':
                        self.logChat(data.cont)
                        self.current(data.cont)
                    else:
                        self.logChat(data.cont)

                    if data.typ == 'export':
                        print("*** Sending chat...")
                        self.exportChat(client_socketObj)
                    elif data.typ == 'help':
                        print("*** Sending command list...")
                        self.sendCommandList(client_socketObj)
                    else:
                        # no need to pack the messages here becaue its done in the 'self.sendMessageToClients' function
                        for connection in self.clientConnections:
                            if connection.socketObj != client_socket:
                                self.sendMessageToClient(connection, data) # broadcasting

    # [utility functions]
    def updateClientConnection(self, target, newName, newKey):
        for connection in self.clientConnections:
            if connection.socketObj == target:
                if newName != None:
                    connection.username = newName
                if newKey != None:
                    connection.encKey = newKey

    # returns the client connection object from a socket object (returns None if none exist)
    def findConnectionFromSocket(self, sockObj):
        for connection in self.clientConnections:
            if connection.socketObj == sockObj:
                return connection
        return None


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

    except KeyboardInterrupt:
        print("*** Closing all the connections ***")
        server.stopServer()
        print("*** Server stopped ***")

    except Exception as e:
        print("General error", str(e))


if __name__ == "__main__":
    main()
