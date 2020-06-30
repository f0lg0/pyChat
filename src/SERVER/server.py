import socket
import json
import threading
import sys
import argparse
import os
from datetime import datetime
from message import Message
from streaming import createMsg, streamData, initializeAES, decryptMsg, returnVector
from clientConnectionObj import ClientConnection
import pyDHE
import time

serverDH = pyDHE.new() # DiffieHellman object

class Server:
    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port

        self.USERNAME = "*server*"

        self.temp_f = False # flag for loop logic

        # holds a list of client connection objects (eventully we should have just this)
        self.clientConnections = []

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

            # instantiate a client connection obj with the username and encrytion key initially set to null
            self.clientConnections.append(ClientConnection(client_socket, None, None))

            cThread = threading.Thread(target = self.handler, args = [self.findConnectionFromSocket(client_socket)])
            cThread.daemon = True
            cThread.start()

            self.shareVector(client_socket, address[0])
            time.sleep(0.1) # to avoid buffer congestion
            self.sharePublicKey(client_socket, address[0])
            time.sleep(0.1) # to avoid buffer congestion

    # exception is the name it should not include (leave blank to get all)
    def generateClientNames(self, exception=None):
        names = []
        for connection in self.clientConnections:
            if exception != None:
                if connection.username != exception:
                    names.append(connection.username)

        return names

    def stopServer(self):
        for conn in self.clientConnections:
            conn.socketObj.close()

        try:
            os.remove(self.current_chat)
        except FileNotFoundError:
            print("*** Nothing to clear in the logs")

        self.server.close()

    def shareVector(self, client_socket, address):
        content = returnVector().decode("utf-8") # returns vector from streaming.py where we get it from encryption, this is base64
        packet = Message(self.IP, address, self.USERNAME, str(datetime.now()), content, 'iv_exc')
        client_socket.send(packet.pack())


    def sharePublicKey(self, client_socket, address):
        packet  = Message(self.IP, address, self.USERNAME, str(datetime.now()), str(serverDH.getPublicKey()), 'key_exc')
        client_socket.send(packet.pack())

    def logCurrentChat(self, username, msg):
        with open(self.current_chat, 'a+') as currentchat:
            currentchat.write(username + "> " + msg + '\n')

    def checkUsername(self, client_socketObj, data):
        flag = False

        for user in self.clientConnections:
            if user.username == data.cont:
                flag = True
                self.temp_f = True

                content = "[*] Username already in use!"

                warning = Message(self.IP, client_socketObj.getIP(), self.USERNAME, str(datetime.now()), content, 'username_taken')

                self.sendMessageToClient(client_socketObj, warning)
                break

        if flag == False:
            client_socketObj.username = data.cont

            content = "[*] You have joined the chat!"

            joined = Message(self.IP, client_socketObj.getIP(), self.USERNAME, str(datetime.now()), content, 'approved_conn')

            self.sendMessageToClient(client_socketObj, joined)
            time.sleep(1) # THIS IS DA FIX FOR EVERYTHING (packet congestion between username and client list)

            # update all others client list
            for connection in self.clientConnections:
                listToSend = self.generateClientNames(connection.username) # return all client names other than the current client (set shouldParseContents to true)
                client_list_update = Message(self.IP, connection.getIP(), self.USERNAME, str(datetime.now()), listToSend, 'client_list_update_add', True)
                self.sendMessageToClient(connection, client_list_update)



    def sendLoggedChat(self, client_socketObj):
        with open(self.current_chat, "rb") as chat:
            content = chat.read().decode("utf-8")

            packet = Message(self.IP, client_socketObj.getIP(), self.USERNAME, str(datetime.now()), content, 'export')

            self.sendMessageToClient(client_socketObj, packet)
            print("[*] Sent!")


    def closeConnection(self, client_socketObj):
        disconnected_msg = f"[{client_socketObj.username}] has left the chat"
        left_msg_obj = Message(self.IP, "allhosts", self.USERNAME, str(datetime.now()), disconnected_msg, 'default')

        self.clientConnections.remove(client_socketObj)

        for connection in self.clientConnections:
            self.sendMessageToClient(connection, left_msg_obj) # sends an alert in chat that they left

            # update everyones clientlist with the new list
            listToSend = self.generateClientNames(connection.username) # return all client names other than the current client (set shouldParseContents to true)
            client_list_update = Message(self.IP, connection.getIP(), self.USERNAME, str(datetime.now()), listToSend, 'disconnection', True)
            self.sendMessageToClient(connection, client_list_update)

        if not self.clientConnections:
            try:
                os.remove(self.current_chat)
            except FileNotFoundError:
                print("*** Nothing to clear in the logs")

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
                client_socketObj.encKey = finalKey
            else:
                if data.cont != '':
                    if data.typ == 'default':
                        self.logCurrentChat(data.username, data.cont)

                    if data.typ == 'export':
                        print("*** Sending chat...")
                        self.sendLoggedChat(client_socketObj)
                    else:
                        # no need to pack the messages here becaue its done in the 'self.sendMessageToClients' function
                        for connection in self.clientConnections:
                            if connection.socketObj != client_socket:
                                self.sendMessageToClient(connection, data) # broadcasting

    # [utility functions]

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
        os.mkdir('./logs')
    except FileExistsError:
        pass

    with open('./logs/currentchat.txt', 'w+') as f:
        f.write("{Start of conversation}\n")
    try:
        options = getArgs()
        PORT = int(options.port)
    except Exception: # if the user doesn't parse values from the command line
        PORT = int(input("*** Start server on port > "))

    HOSTNAME = socket.gethostname()
    IP =  socket.gethostbyname(HOSTNAME)

    server = Server(IP, PORT)

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
