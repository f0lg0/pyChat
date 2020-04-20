import json
import base64
from encryption import RSAEncryption
from Crypto.Cipher import PKCS1_OAEP # RSA based cipher using Optimal Asymmetric Encryption Padding


BUFFERSIZE = 10
enc = RSAEncryption(1024)

enc.generatePrivateKey()
print("*** Generated private key ***")

enc.writeToFile()

priv_key = enc.importPrivate()
pub_key = enc.importPublic()

priv_cipher = PKCS1_OAEP.new(key = priv_key)
pub_cipher = PKCS1_OAEP.new(key=pub_key)

# generates a message with a fixed header which specifies the length of the message (returns bytes)
def createMsg(data):
    data = data.encode("utf-8")
    print(len(data))
    
    # encrypting with private
    data = priv_cipher.encrypt(data)
    print("\nEncrypted with PRIV ", data)
    print(len(data))


    # ecnrypting with public
    data = pub_cipher.encrypt(data)
    print("\nEncrypted with PUB ", data)


    finalMsg = base64.b64encode(data).decode("utf-8")
    finalMsg = f'{len(finalMsg):<10}' + finalMsg
    return finalMsg.encode("utf-8")


def streamData(target):
    data = target.recv(BUFFERSIZE)
    if len(data) != 0:
        msglen = int(data[:BUFFERSIZE].strip())
        full_data = b''

        # stream the data in with a set buffer size
        while len(full_data) < msglen:
            full_data += target.recv(BUFFERSIZE)

        if "key_exc" not in full_data.decode("utf-8"):
            full_data = base64.b64decode(full_data)
            full_data = priv_cipher.decrypt(full_data)
            full_data = pub_cipher.decrypt(full_data)


        return full_data # returning just the bytes, json operations done later in the code to avoid importing errors
    else:
        pass