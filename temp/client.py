import socket
import pickle
import threading
import sys
import time
from datetime import datetime
from displayBanner import displayBanner
from msgManager import createMsg
from msgManager import streamData

HEADERSIZE = 10

class Client:
    def __init__(self, server_ip, port, buffer_size, client_ip):
        self.SERVER_IP = server_ip
        self.PORT = port
        self.BUFFER_SIZE = buffer_size
        self.CLIENT_IP = client_ip

        self.export = False
        self.help = False

        print(f"[*] Host: {self.CLIENT_IP} | Port: {self.PORT}")

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connectToServer(self):
        try:
            self.client.connect((self.SERVER_IP, self.PORT))
        except socket.error as e:
            print(str(e))
            sys.exit()

        self.setUsername()

    def setUsername(self):
        while True:
            self.USERNAME = input("Enter username> ")
            if self.USERNAME:
                #self.client.sendall("[usr]".encode("utf-8") + self.USERNAME.encode("utf-8"))
                print(int(createMsg("[usr]" + self.USERNAME)[:HEADERSIZE].strip()))
                self.client.sendall(createMsg("[usr]" + self.USERNAME))

                check = self.client.recv(self.BUFFER_SIZE)
                print(check.decode("utf-8"))

                if check.decode("utf-8") != "Username already in use!":
                    break

            else:
                print("Username can't be empty!")


    def sendMsg(self):
        self.to_send_msg = ""
        while True:
            self.to_send_msg = input("You> ")

            if self.to_send_msg == "[export_chat]":
                self.export = True
            elif self.to_send_msg == "[help]":
                self.help = True

            if self.to_send_msg:
                self.client.sendall(createMsg("> ".join([self.USERNAME, self.to_send_msg])))
                self.to_send_msg = ""
                self.sent = False
            else:
                print("Cant send empty message!")


    def receiveData(self):
        iThread = threading.Thread(target = self.sendMsg)
        iThread.daemon = True
        iThread.start()

        while True:
            print(self.client, self.BUFFER_SIZE)
            data = streamData(self.client, self.BUFFER_SIZE)

            if not data:
                print("[*] Connection closed by the server")
                sys.exit()

            if self.export == True:
                timestamp = datetime.now()
                chat_file = f"./exported/chat{str(timestamp)}.txt"
                print(chat_file)

                try:
                    with open(chat_file, "w+") as chat:
                        chat.write(data.decode("utf-8"))
                        print("[*] Writing to file...")

                    print(f"[*] Finished! You can find the file at {chat_file}")
                    self.export = False
                    print('\n' + "You> ", end = "")
                except:
                    self.export = False
                    print('\r' + "[*] Something went wrong" + '\n' + "You> ", end = "")
            else:
                if self.help == True:
                    cdict = pickle.loads(data)
                    for command in cdict:
                        print('\r' + command + " : " + cdict[command])

                    print('\r' + "You> ", end = "")
                else:
                    print('\r' + data.decode("utf-8") + '\n' + "You> ", end = "")



def main():
    displayBanner()

    SERVER_IP = input("[*] Enter server's IP> ")
    PORT = int(input("[*] Enter port> "))
    BUFFER_SIZE = 10

    CLIENT_IP = socket.gethostname()

    client = Client(SERVER_IP, PORT, BUFFER_SIZE, CLIENT_IP)
    client.connectToServer()
    client.receiveData()


if __name__ == "__main__":
    main()
