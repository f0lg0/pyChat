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
    cont: str
    typ: str

    def pack(self):
        return createMsg(self.to_json())
