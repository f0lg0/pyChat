import pickle

BUFFERSIZE = 10

#generates a message with a fixed header which specifies the length of the message 
def createMsg(data):
    finalMsg = data
    finalMsg = f'{len(finalMsg):<10}'.encode("utf-8") + finalMsg
    return finalMsg


def streamData(target):
    data = target.recv(BUFFERSIZE)
    print("recv: ", data)

    if len(data) != 0: # f0lg0: TEMP FIX -> if a client disconnects the server will receive an empty msg so we skip this shit, it will return none
        msglen = int(data[:BUFFERSIZE].strip())
        decoded_data = b''

        #stream the data in with a set buffer size
        while len(decoded_data) < msglen:
            decoded_data += target.recv(BUFFERSIZE)
        
        obj = pickle.loads(decoded_data)

        # f0lg0: TEMP FIX: this is what caused your problem, after the username thing contents are already strings so you were decoding strings, currently dunno where they got set in strings. We should always keep everything in bytes tho
        try:
            obj.cont = obj.cont.decode("utf-8")
        except:
            pass

        return obj
    



    