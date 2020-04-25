#Note that I've only modified this file, client and server remain unchanged

import json
import base64
from encryption import AESEncryption

BUFFERSIZE = 10
PASSWORD = b'password'

enc = AESEncryption(PASSWORD)

def exportVector():
    enc.writeVectorToFile()

# generates a message with a fixed header which specifies the length of the message (returns bytes)
def createMsg(data):
    if "iv_exc" not in data and "key_exc" not in data:
        cipher = enc.generateCipher() # everytime we generate a object, it can't be reused 
        encrypted_data = base64.b64encode(cipher.encrypt(data.encode("utf-8"))) # base64 rappresents bytes object in strings
        print("\nENCRYPTED DATA ", base64.b64decode(encrypted_data))


        finalMsg = encrypted_data.decode("utf-8")
        finalMsg = f'{len(finalMsg):<10}' + finalMsg

        print("\nCRAFTED ", finalMsg.encode("utf-8"))
        return finalMsg.encode("utf-8")
    else:
        finalMsg = data
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

        if "iv_exc" not in full_data.decode("utf-8") and "key_exc" not in full_data.decode("utf-8"):
            print("hit")
            cipher = enc.generateCipher() # everytime we generate a object, it can't be reused 

            print("\nRECV BASE64 ALREADY STRIPPED FROM HEADER", full_data)
            full_data = base64.b64decode(full_data)
            print("\nRECV BASE64 DEC ", full_data)


            decrypted_data = cipher.decrypt(full_data)
        
            return decrypted_data # returning just the bytes, json operations done later in the code to avoid importing errors
        return full_data
    else:
        pass
