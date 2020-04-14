import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from streaming import createMsg, streamData

@dataclass_json
@dataclass
class Message:
    shost: str
    dhost: str
    username: str # of the sender
    date: str
    cont: bytes
    typ: str

    def pack(self):
        return createMsg(self.to_json())



'''
class Message:
    def __init__(self, shost, dhost, username, date, cont, typ):
        self.shost = shost
        self.dhost = dhost
        self.username = username
        self.date = date
        self.cont = cont
        self.typ = typ
    
    def pack(self):
        return createMsg(json.dumps(self))
'''