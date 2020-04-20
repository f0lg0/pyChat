from Crypto.PublicKey import RSA #  to generate the keys

class RSAEncryption:
    def __init__(self, bits):
        self.BITS = bits

    def generatePrivateKey(self):
        self.private_key = RSA.generate(self.BITS)

    def generatePublicKey(self):
        self.public_key = self.private_key.publickey()

    def writeToFile(self):
        private_pem = self.private_key.exportKey().decode("utf-8")
        public_pem = self.public_key.exportKey().decode("utf-8")

        with open('./keys/private.pem', 'w+') as private:
            private.write(private_pem)

        with open('./keys/public.pem', 'w+') as private:
            private.write(public_pem)

    def importKeys(self):
        keys = []
        pr_key = RSA.importKey(open('./keys/private.pem', 'r').read())
        pu_key = RSA.importKey(open('./keys/public.pem', 'r').read())

        keys.append(pr_key)
        keys.append(pu_key)

        return keys