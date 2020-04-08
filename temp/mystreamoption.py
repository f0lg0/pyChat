
    # try to update the buffer with recv sized
    def updateBuffer(self, size):
        buff = ""
        for counter in range(0, len(size)):
            if size[counter].isdigit():
                buff += size[counter]

        return int(buff)

    # for files bigger than buffer
    def saveBigFile(self, size, buff):
        full = b''
        while True:
            if sys.getsizeof(full) >= size:
                break

            recvfile = self.client_socket.recv(buff)

            full += recvfile

        return full
