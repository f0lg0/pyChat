import pickle
import json
import jsons
from dataclasses import dataclass
from streaming import createMsg, streamData

@dataclass
class Message:
    shost: str
    dhost: str
    username: str # of the sender
    date: str
    cont: str
    typ: str

    def pack(self):
        print(type(self.__dict__))
        return createMsg(json.dumps(self.__dict__)) # converting it to a dictionary
