import socket
import pickle
import threading
import argparse
import sys
import time
from datetime import datetime
from displayBanner import displayBanner
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
                enc_username  = self.USERNAME.encode("utf-8")

                packet = Message(self.CLIENT_IP, self.SERVER_IP, "temp", str(datetime.now()), enc_username, len(enc_username), 'setuser')

                self.client.send(packet.pack())
                check = self.client.recv(self.BUFFER_SIZE)
                loaded = pickle.loads(check)
                print(loaded.cont.decode("utf-8"))

                if loaded.cont.decode("utf-8") != "[*] Username already in use!":
                    break

            else:
                print("Username can't be empty!")


    def sendMsg(self):
        while True:
            to_send_msg = input("You> ")

            if to_send_msg:
                enc_msg = to_send_msg.encode("utf-8")
                if to_send_msg == "[export_chat]":
                    self.export = True
                    packet = Message(self.CLIENT_IP, self.SERVER_IP, self.USERNAME, str(datetime.now()), enc_msg, len(enc_msg), 'export')
                elif to_send_msg == "[help]":
                    self.help = True
                    packet = Message(self.CLIENT_IP, self.SERVER_IP, self.USERNAME, str(datetime.now()), enc_msg, len(enc_msg), 'help')
                else:
                    packet = Message(self.CLIENT_IP, self.SERVER_IP, self.USERNAME, str(datetime.now()), enc_msg, len(enc_msg), 'default')

                self.client.send(packet.pack())
                to_send_msg = ""
            else:
                print("Cant send empty message!")


    def receiveData(self):
        iThread = threading.Thread(target = self.sendMsg)
        iThread.daemon = True
        iThread.start()

        while True:
            data = self.client.recv(self.BUFFER_SIZE)
            loaded = pickle.loads(data)

            if not data:
                print("[*] Connection closed by the server")
                sys.exit()

            if self.export == True:
                timestamp = datetime.now()
                chat_file = f"./exported/chat{str(timestamp)}.txt"

                try:
                    with open(chat_file, "wb+") as chat:
                        chat.write(loaded.cont)
                        print("[*] Writing to file...")

                    print(f"[*] Finished! You can find the file at {chat_file}")
                    self.export = False
                    print('\n' + "You> ", end = "")
                except:
                    self.export = False
                    print('\r' + "[*] Something went wrong" + '\n' + "You> ", end = "")
            else:
                if self.help == True:
                    for command in loaded:
                        print('\r' + command + " : " + loaded[command])

                    print('\r' + "You> ", end = "")
                    self.help = False
                else:
                    print('\r' + loaded.username + "> " + loaded.cont.decode("utf-8") + '\n' + "You> ", end = "")


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

    displayBanner()

    CLIENT_IP = socket.gethostname()

    client = Client(SERVER_IP, PORT, BUFFER_SIZE, CLIENT_IP)
    client.connectToServer()
    client.receiveData()


if __name__ == "__main__":
    main()
