import socket
import json
import threading
import argparse
import sys
import time
from datetime import datetime
from message import Message
from streaming import createMsg, streamData, initializeAES
import pyDHE


clientDH = pyDHE.new()

# from displayBanner import displayBanner

class Client:
    def __init__(self, server_ip, port, buffer_size, client_ip):
        self.SERVER_IP = server_ip
        self.PORT = port
        self.BUFFER_SIZE = buffer_size
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

        iv = self.recvVector()
        self.finalDecryptionKey = self.recvServerKey()
        print(self.finalDecryptionKey)
        print("*** Got vector ***")
        with open('./vector', 'wb+') as f:
            f.write(iv.cont.encode("utf-8"))

        self.sharePublicInfo()
        initializeAES()
        self.setUsername()

    def recvServerKey(self):
        #receives the servers public key and uses it to generate the final decryption key
        serverKey = Message.from_json(streamData(self.client).decode("utf-8"))
        return clientDH.update(int(serverKey.cont))

    def sharePublicInfo(self):
        packet  = Message(self.CLIENT_IP, self.SERVER_IP, "temp", str(datetime.now()), str(clientDH.getPublicKey()), 'key_exc')
        self.client.send(packet.pack())
        
        print("sent", packet.pack())
        print("*** Client's Public Key Sent ***")


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
                    print("\nSENT ", packet.pack())

                    check = streamData(self.client).decode("utf-8")
                    check = Message.from_json(check)
                    print("\nRECV AES DEC", check)
                    print(check.cont)

                    if check.cont != "[*] Username already in use!":
                        break

                else:
                    print("Can't set username as *server*!")

            else:
                print("Username can't be empty!")


    def sendMsg(self):
        while True:
            to_send_msg = input("You> ")
            if to_send_msg:
                if to_send_msg == "[export_chat]":
                    packet = Message(self.CLIENT_IP, self.SERVER_IP, self.USERNAME, str(datetime.now()), to_send_msg, 'export')
                elif to_send_msg == "[help]":
                    packet = Message(self.CLIENT_IP, self.SERVER_IP, self.USERNAME, str(datetime.now()), to_send_msg, 'help')
                else:
                    packet = Message(self.CLIENT_IP, self.SERVER_IP, self.USERNAME, str(datetime.now()), to_send_msg, 'default')

                self.client.send(packet.pack())
                print("\rSENT ", packet.pack())
                to_send_msg = ""
            else:
                print("Cant send empty message!")


    def receiveData(self):
        iThread = threading.Thread(target = self.sendMsg)
        iThread.daemon = True
        iThread.start()

        while True:
            try:
                data = streamData(self.client)
                print("\rRECV AFTER AES DEC ", data)
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
                    print('\n' + "You> ", end = "")
                except:
                    print('\r' + "[*] Something went wrong" + '\n' + "You> ", end = "")
            else:
                if data.typ == "help":
                    for command in data.cont:
                        print('\r' + command + " : " + data.cont[command])

                    print('\r' + "You> ", end = "")
                else:
                    print('\r' + data.username + "> " + data.cont + '\n' + "You> ", end = "")

        self.client.close()

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

def main():
    try:
        options = getArgs()

        SERVER_IP = options.server_ip
        PORT = int(options.server_port)
    except Exception: # in case the user doesn't provide values we ask him to enter them
        SERVER_IP = input("*** Enter server IP address > ")
        PORT = int(input("*** Enter server PORT number > "))

    BUFFER_SIZE = 1024

    # displayBanner()

    CLIENT_IP = socket.gethostbyname(socket.gethostname())

    client = Client(SERVER_IP, PORT, BUFFER_SIZE, CLIENT_IP)
    client.connectToServer()
    client.receiveData()


if __name__ == "__main__":
    main()
