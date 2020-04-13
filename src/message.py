import pickle
from dataclasses import dataclass
from streaming import createMsg, streamData

@dataclass
class Message:
    shost: str
    dhost: str
    username: str # of the sender
    date: str
    cont: bytes
    typ: str

    def pack(self):
        return createMsg(pickle.dumps(self))
