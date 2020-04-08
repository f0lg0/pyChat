#Will add a fixed header and return a sendable string (we should add pickle support here at some point somehow), also encodes the message for you

def createMsg(data):
    msg = data
    msg = f'{len(msg):<10}' + msg
    return msg.encode("utf-8")

#streams data from the 'target' socket with an initial buffersize of 'bufferSize' (returns the decoded data)
def streamData(target, bufferSize):
    #initial data chunk (contains an int of how much data the server should expect)
    
    data = target.recv(bufferSize)

    msglen = int(data[:bufferSize].strip())
    decoded_data = ''

    #stream the data in with a set buffer size
    while len(decoded_data) < msglen:
        print(decoded_data)
        decoded_data += target.recv(bufferSize).decode("utf-8")
    
    return decoded_data


    
    
        


