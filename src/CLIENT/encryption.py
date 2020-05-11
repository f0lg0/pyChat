from Crypto.Cipher import AES 
import hashlib
from Crypto import Random
import base64

class AESEncryption:
    def __init__(self, password, vector): # vector here is base64
        self.PASSWORD = password
        self.KEY = hashlib.sha256(self.PASSWORD).digest() # generating a 32 bytes key 
        self.IV = base64.b64decode(vector) # initialization vector, we need to make this random. It can be shared in plain text, it's not secret

        self.MODE = AES.MODE_CFB # automatic padding mode (?)

    def generateCipher(self):
        return AES.new(self.KEY, self.MODE, IV = self.IV)


class DiffieHellman:
    def __init__(self, sharedBase, sharedPrime):
        self.sharedBase = sharedBase
        self.sharedPrime = sharedPrime