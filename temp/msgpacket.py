from dataclasses import dataclass
from datetime import datetime

import socket
import pickle # pickle should always be the preferred way to serialize Python objects. -> ref https://docs.python.org/3/library/pickle.html

@dataclass
class Message:
    shost: str
    dhost: str
    date: str
    cont: bytes
    size: int
    typ: str

    def pack(self):
        return pickle.dumps(self) # it's already in bytes, no need to encode

    def send(self):
        packet = self.pack()
        print("\nPacked packet > ", packet) # packed packet in bytes -> this is for debug 

        return packet
        # send here with socket.sendall / socket.send

def main():
    CLIENT_IP = socket.gethostbyname(socket.gethostname())

    timestamp = datetime.now()
    print("[ SENDER ]")
    content = input("\n*** Send a message > ")
    typ = ""

    # it won't be like this, this is just a test to define the typ field. The user won't actually type the tags inside the message
    if "[usr]" in content:
        typ = "user-request"
    elif "[export_chat]" in content:
        typ = "export-request"
    else:
        typ = "default"


    # sender code
    msg = Message(CLIENT_IP, "destination", f"{str(timestamp)}", content, len(content), typ) # with default I mean that the message is not a thing like [usr] or [export_chat], the message will be already encoded in bytes

    print("*** SENDING MESSAGE ***")
    packet = msg.send() # this shouldn't have a return but i am doing to simulate a receiver
    print("\n*** SENT ***")

    # receiver code
    print("[ RECEIVER ]")
    recv = pickle.loads(packet)

    print("\n*** GOT PACKET ***")
    print("\nLoaded packet > ", recv)

    print("\n*** Received message > ", recv.cont)

    """

    if we use fixed length headers then we don't need size, if we use my method then we need it. 
    I feel like fixed length header are not safe, you can still cause damage by sending huge stuff. 
    My method otherwise keeps receiving stuff until it got everything, as you said maybe there will be problems like pakcet congestion and stuff.
    If we plan to include images then we should use my method, on the other hand fixed lenght headers are great. We can use both at the same time

    """


    """
    USEFUL OUTPUT 

    [ SENDER ]

    *** Send a message > this is a test
    *** SENDING MESSAGE ***

    Packed packet >  b'\x80\x03c__main__\nMessage\nq\x00)\x81q\x01}q\x02(X\x05\x00\x00\x00shostq\x03X\x0c\x00\x00\x00192.168.1.39q\x04X\x05\x00\x00\x00dhostq\x05X\x0b\x00\x00\x00destinationq\x06X\x04\x00\x00\x00dateq\x07X\x1a\x00\x00\x002020-04-09 11:21:24.955955q\x08X\x04\x00\x00\x00contq\tX\x0e\x00\x00\x00this is a testq\nX\x04\x00\x00\x00sizeq\x0bK\x0eX\x03\x00\x00\x00typq\x0cX\x07\x00\x00\x00defaultq\rub.'

    *** SENT ***
    [ RECEIVER ]

    *** GOT PACKET ***

    Loaded packet >  Message(shost='192.168.1.39', dhost='destination', date='2020-04-09 11:21:24.955955', cont='this is a test', size=14, typ='default')

    *** Received message >  this is a test)


    """

if __name__ == "__main__":
    main()