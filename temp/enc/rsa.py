from Crypto.Cipher import PKCS1_OAEP # RSA based cipher using Optimal Asymmetric Encryption Padding
from Crypto.PublicKey import RSA #  to generate the keys
from binascii import hexlify # to convert encrypted cipher to hexadecimal format

message = b'This is a test'

# generating 1024bit private key
private_key = RSA.generate(1024)

# generating public key from tyhe private one
public_key = private_key.publickey()

# converting the RSAkey objects to string
private_pem = private_key.exportKey().decode()
public_pem = public_key.exportKey().decode()

with open("./private.pem", "w+") as private:
    private.write(private_pem)

with open("./public.pem", "w+") as public:
    public.write(public_pem)

# Importing keys from files, converting it into the RsaKey object
pr_key = RSA.importKey(open('private.pem', 'r').read())
pu_key = RSA.importKey(open('public.pem', 'r').read())

print(pr_key)
print(pu_key)

# Instantiating PKCS1_OAEP object with the public key for encryption
cipher = PKCS1_OAEP.new(key=pu_key)
# Encrypting the message with the PKCS1_OAEP object
cipher_text = cipher.encrypt(message)
print(bytes(cipher_text))

# Instantiating PKCS1_OAEP object with the private key for decryption
decrypt = PKCS1_OAEP.new(key=pr_key)
# Decrypting the message with the PKCS1_OAEP object
decrypted_message = decrypt.decrypt(cipher_text)
print(decrypted_message)
