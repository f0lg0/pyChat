import pickle
from dataclasses import dataclass

@dataclass
class Message:
    shost: str
    dhost: str
    username: str # of the sender
    date: str
    cont: bytes
    size: int
    typ: str

    def pack(self):
        return pickle.dumps(self)