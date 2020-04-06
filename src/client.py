import socket
import pickle
import threading
import argparse
import sys
import time
from datetime import datetime
from displayBanner import displayBanner

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
                self.client.sendall("[usr]".encode("utf-8") + self.USERNAME.encode("utf-8"))
                check = self.client.recv(self.BUFFER_SIZE)
                print(check.decode("utf-8"))

                if check.decode("utf-8") != "Username already in use!":
                    break

            else:
                print("Username can't be empty!")


    def sendMsg(self):
        to_send_msg = ""
        while True:
            to_send_msg = input("You> ")

            if to_send_msg == "[export_chat]":
                self.export = True
            elif to_send_msg == "[help]":
                self.help = True

            if to_send_msg:
                self.client.sendall(bytes("> ".join([self.USERNAME, to_send_msg]), "utf-8"))
                to_send_msg = ""
                self.sent = False
            else:
                print("Cant send empty message!")


    def receiveData(self):
        iThread = threading.Thread(target = self.sendMsg)
        iThread.daemon = True
        iThread.start()

        while True:
            data = self.client.recv(self.BUFFER_SIZE)

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
                    self.help = False
                else:
                    print('\r' + data.decode("utf-8") + '\n' + "You> ", end = "")


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", dest = "server_ip", help = "Enter server IP")
    parser.add_argument("-p", "--port", dest = "server_port", help = "Enter server PORT")

    options = parser.parse_args()

    if not options.server_ip:
        parser.error("*** Please specify a server IP ***")
    elif not options.server_port:
        parser.error("*** Please specify a port number ***")
    else:
        return options

def main():
    options = getArgs()

    SERVER_IP = options.server_ip
    PORT = int(options.server_port)

    BUFFER_SIZE = 1024

    displayBanner()

    CLIENT_IP = socket.gethostname()

    client = Client(SERVER_IP, PORT, BUFFER_SIZE, CLIENT_IP)
    client.connectToServer()
    client.receiveData()


if __name__ == "__main__":
    main()
