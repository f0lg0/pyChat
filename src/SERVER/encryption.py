import socket
import hashlib
import base64
from Crypto.Cipher import AES 
from Crypto import Random

IV = None # vector is global, we start with None
def generateVector():
	global IV

	if IV == None: # if it's the first time that we generate it then go ahead
		IV = Random.new().read(AES.block_size) # we save it as bytes

	return base64.b64encode(IV) # initialization vector, we need to make this random. It can be shared in plain text, it's not secret. We return the base64


class AESEncryption:
    def __init__(self, password):
        self.PASSWORD = password
        self.KEY = hashlib.sha256(self.PASSWORD).digest() # generating a 32 bytes key 

        self.MODE = AES.MODE_CFB # automatic padding mode (?)

    def generateCipher(self):
        return AES.new(self.KEY, self.MODE, IV = IV) # so here we can grab the unique vector






