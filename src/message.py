import json
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from streaming import createMsg, streamData

#will parse the contents if the 
@dataclass_json
@dataclass
class Message:
    shost: str
    dhost: str
    username: str # of the sender
    date: str
    cont: str
    typ: str
    shouldParseContents: bool = False

    if shouldParseContents:
        if type(cont) == str:
            shouldParseContents = json.loads(cont)
        else:
            shouldParseContents = json.dumps(cont)

    #Note that shouldParseContents variable only works with pythons built in objects, not dynamically created ones
    def pack(self):
        return createMsg(self.to_json())
