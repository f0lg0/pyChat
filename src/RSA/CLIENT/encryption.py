from Crypto.PublicKey import RSA

class RSAEncryption:
    def __init__(self, bits):
        self.BITS = bits

    def generatePrivateKey(self):
        self.private_key = RSA.generate(self.BITS)


    def writeToFile(self):
        private_pem = self.private_key.exportKey().decode("utf-8")

        with open('./keys/private.pem', 'w+') as private:
            private.write(private_pem)

    def importPrivate(self):
        pr_key = RSA.importKey(open('./keys/private.pem', 'r').read())
        return pr_key

    def importPublic(self):
        pub_key = RSA.importKey(open("./keys/public.pem", 'r').read())
        return pub_key