from Crypto.Cipher import AES 
import hashlib
from Crypto import Random
import base64

class AESEncryption:
    def __init__(self, password):
        self.PASSWORD = password
        print("* PASSWORD: ", self.PASSWORD)

        self.KEY = hashlib.sha256(self.PASSWORD).digest() # generating a 32 bytes key 
        
        with open('./vector', 'rb+') as f:
        	self.IV = base64.b64decode(f.read()) # initialization vector, we need to make this random. It can be shared in plain text, it's not secret
        
        print("VECTOR ", self.IV)
        self.MODE = AES.MODE_CFB # automatic padding mode (?)

    def generateCipher(self):
        return AES.new(self.KEY, self.MODE, IV = self.IV)


class DiffieHellman:
    def __init__(self, sharedBase, sharedPrime):
        self.sharedBase = sharedBase
        self.sharedPrime = sharedPrime