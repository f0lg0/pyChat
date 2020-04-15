import pickle
import dataclasses
from dataclasses import dataclass
from streaming import createMsg, streamData

import json

@dataclass
class Message:
    shost: str
    dhost: str
    username: str # of the sender
    date: str
    cont: str
    typ: str

    def pack(self):
        print("[CRAFTED]", json.dumps(self, cls=EnhancedJSONEncoder))
        return createMsg(json.dumps(self, cls=EnhancedJSONEncoder))


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

