from Crypto.Cipher import AES 
import hashlib

class AESEncryption:
    def __init__(self, password):
        self.PASSWORD = password

        self.KEY = hashlib.sha256(self.PASSWORD).digest() # generating a 32 bytes key 
        self.IV = 16 * b'\x00' # initialization vector, we need to make this random. It can be shared in plain text, it's not secret
        self.MODE = AES.MODE_CFB # automatic padding mode (?)

    def generateCipher(self):
        return AES.new(self.KEY, self.MODE, IV = self.IV)