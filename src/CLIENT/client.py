import socket
import json
import threading
import argparse
import sys
import os
import time
from datetime import datetime
from message import Message
from streaming import createMsg, streamData, initializeAES
import pyDHE
import eel

# this is temporary, just for debuggining when you want to open two clients on one computer
# Note that there is a small chance the random port numbers will be the same and crash anyway.
import random

# [GLOBAL VARIABLES]
client = None # so we can use it in exposed functions
eel.init('./GUI/web') # initializing eel
eelPort = 42069 # default GUI port

clientDH = pyDHE.new() # diffiehellman object

# contains names only of all the clients connected
client_list = [];

class Client:
    def __init__(self, server_ip, port, client_ip):
        self.SERVER_IP = server_ip
        self.PORT = port
        self.CLIENT_IP = client_ip
        self.finalDecryptionKey = None

        print(f"[*] Host: {self.CLIENT_IP} | Port: {self.PORT}")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connectToServer(self):
        try:
            self.client.connect((self.SERVER_IP, self.PORT))
        except socket.error as e:
            print(str(e))
            sys.exit()

        iv = self.recvVector() # we receive the vector
        finalDecryptionKey = self.recvServerKey()

        self.sharePublicInfo()
        initializeAES(str(finalDecryptionKey).encode("utf-8"), iv.cont) # we even parse the vector message content
        self.setUsername()

    def recvServerKey(self):
        # receives the servers public key and uses it to generate the final decryption key
        serverKey = Message.from_json(streamData(self.client).decode("utf-8"))
        return clientDH.update(int(serverKey.cont))

    def sharePublicInfo(self):
        packet  = Message(self.CLIENT_IP, self.SERVER_IP, "temp", str(datetime.now()), str(clientDH.getPublicKey()), 'key_exc')
        self.client.send(packet.pack())

    def recvVector(self):
        iv = streamData(self.client).decode("utf-8")
        return Message.from_json(iv)

    def setUsername(self):
        while True:
            self.USERNAME = input("Enter username> ")
            if self.USERNAME:
                if self.USERNAME != "*server*":
                    # encrypted_username = self.cipher.encrypt(self.USERNAME.encode("utf-8"))
                    packet = Message(self.CLIENT_IP, self.SERVER_IP, "temp", str(datetime.now()), self.USERNAME, 'setuser')

                    self.client.send(packet.pack())

                    check = streamData(self.client).decode("utf-8")
                    check = Message.from_json(check)
                    print(check.cont)

                    if check.cont != "[*] Username already in use!":
                        break

                else:
                    print("Can't set username as *server*!")

            else:
                print("Username can't be empty!")


    def sendMsg(self, to_send_msg):
        if to_send_msg == "[export_chat]":
            packet = Message(self.CLIENT_IP, self.SERVER_IP, self.USERNAME, str(datetime.now()), to_send_msg, 'export')
        else:
            packet = Message(self.CLIENT_IP, self.SERVER_IP, self.USERNAME, str(datetime.now()), to_send_msg, 'default')

        self.client.send(packet.pack())

    def receiveData(self):
        while True:
            try:
                data = streamData(self.client)
                data = data.decode("utf-8")
                data = Message.from_json(data) # it's a dataclass object
            except AttributeError:
                print("\r[*] Connection closed by the server")
                break

            if data.typ == "export":
                timestamp = str(datetime.now())
                timestamp = timestamp.replace(":", ".") # windowz is stoopid

                chat_file = f"./exported/chat{timestamp}.txt"

                try:
                    with open(chat_file, "wb+") as chat:
                        chat.write(data.cont.encode("utf-8"))
                        print("\r[*] Writing to file...")

                    print(f"[*] Finished! You can find the file at {chat_file}")
                except:
                    print('\r' + "[*] Something went wrong")
            elif data.typ == "client_list_update_add" or data.typ == "disconnection":
                updateClientList(data.cont)
            else:
                eel.writeMsg(data.cont, data.username)

        self.client.close()


# updates the gui with the list 'c_list'
def updateClientList(c_list):
    client_list = c_list;

    # update the GUI
    eel.updateClientList(client_list);


# [Eel functions]
# we need to set a name scheme for these functions cuz rn they are confusing
@eel.expose
def exposeSendMsg(to_send_msg):
    client.sendMsg(to_send_msg)

@eel.expose
def getUsername():
    return client.USERNAME


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", dest = "server_ip", help = "Enter server IP")
    parser.add_argument("-p", "--port", dest = "server_port", help = "Enter server PORT")

    options = parser.parse_args()

    if not options.server_ip and not options.server_port:
        raise Exception # raising exception in case the user doesn't provide values from the terminal

    if not options.server_ip:
        parser.error("*** Please specify a server IP ***")
    elif not options.server_port:
        parser.error("*** Please specify a port number ***")
    else:
        return options



def startEel():
    try:
        # eel.start('main.html', port=random.choice(range(8000, 8080))) --> use this if you want to open multiple clients on one computer
        eel.start('main.html', port=eelPort)
    except EnvironmentError:
        eel.start('main.html', port=eelPort, mode='default')
    except (SystemExit, MemoryError, KeyboardInterrupt): # this catches the exception thrown if the user closes the window
        print("*** Closing the app... ***")
        os._exit(0)  # this is actually super overkill but it works

def main():
    try:
        os.mkdir('./exported')
    except FileExistsError:
        pass

    try:
        options = getArgs()

        SERVER_IP = options.server_ip
        PORT = int(options.server_port)
    except Exception: # in case the user doesn't provide values we ask him to enter them
        SERVER_IP = input("*** Enter server IP address > ")
        PORT = int(input("*** Enter server PORT number > "))

    CLIENT_IP = socket.gethostbyname(socket.gethostname())


    global client
    client = Client(SERVER_IP, PORT, CLIENT_IP)
    client.connectToServer()

    # threding eel in the background
    eThread = threading.Thread(target = startEel)
    eThread.daemon = True
    eThread.start()


    client.receiveData() # this is a loop and also streamData is blocking


if __name__ == "__main__":
    try:
        # checking if port 42069 (default port for the GUI) is free to start the GUI
        tempSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        check = tempSock.bind(('127.0.0.1', eelPort))
        tempSock.close()

        main()
    except socket.error as e:
        print(f"[!] PORT NUMBER {eelPort} ISN'T FREE, YOU CAN'T START THE APP [!]")
