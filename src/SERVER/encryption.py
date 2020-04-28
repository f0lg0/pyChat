import socket
import hashlib
import base64
from Crypto.Cipher import AES 
from Crypto import Random

IV = Random.new().read(AES.block_size) # initialization vector, we need to make this random. It can be shared in plain text, it's not secret
with open('./vector', 'wb+') as f:
    f.write(base64.b64encode(IV))

class AESEncryption:
    def __init__(self, password):
        self.PASSWORD = password
        print("* PASSWORD: ", self.PASSWORD)
        self.KEY = hashlib.sha256(self.PASSWORD).digest() # generating a 32 bytes key 

        print("* USING VECTOR ", IV)
        self.MODE = AES.MODE_CFB # automatic padding mode (?)

    def generateCipher(self):
        return AES.new(self.KEY, self.MODE, IV = IV)






