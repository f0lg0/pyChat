import pickle
from dataclasses import dataclass

# f0lg0: removed the size field
@dataclass
class Message:
    shost: str
    dhost: str
    username: str # of the sender
    date: str
    cont: bytes
    typ: str

    def pack(self):
        return pickle.dumps(self)