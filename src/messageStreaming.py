import pickle

BUFFERSIZE = 10

#generates a message with a fixed header which specifies the length of the message 
def createMsg(data):
    finalMsg = data
    finalMsg = f'{len(finalMsg):<10}'.encode("utf-8") + finalMsg
    return finalMsg


def streamData(target):
    data = target.recv(BUFFERSIZE)
    print(data)
    msglen = int(data[:BUFFERSIZE].strip())
    decoded_data = b''

    #stream the data in with a set buffer size
    while len(decoded_data) < msglen:
        decoded_data += target.recv(BUFFERSIZE)
    
    obj = pickle.loads(decoded_data)
    obj.cont = obj.cont.decode("utf-8")

    return obj
    



    