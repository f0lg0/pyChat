# This class stores all the nessacary information for a client connection all in a single object

class ClientConnection:
    def __init__(self, socketObj, username, encKey):
        self.socketObj = socketObj
        self.username = username
        self.encKey = encKey

    #returns the clients address
    def getIP(self):
        return self.socketObj.getsockname()[0]
    
