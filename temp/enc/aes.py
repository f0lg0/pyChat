from Crypto.Cipher import AES
import hashlib

print("*** AES-256 Encryption ***\n[!] Note that everything is in bytes")

password = b'cookie'
print(f"\n* Using {password} as password")

key = hashlib.sha256(password).digest() # to generate 32 byte key so we don't worry about padding the password
print(f"* Generated 32bytes key {key} from hashing {password}")

IV = 16 * b'\x00' # In cryptography, an initialization vector (IV) or starting variable (SV)[1] is a fixed-size input to a cryptographic primitive that is typically required to be random or pseudorandom. Randomization is crucial for encryption schemes to achieve semantic security, a property whereby repeated usage of the scheme under the same key does not allow an attacker to infer relationships between segments of the encrypted message.
print(f"\n* Initialization Vector {IV}")

mode = AES.MODE_CFB # AES.MODE_CBC -> mode with padding and shit
print("* Using CFB mode so we don't worry about padding data")

encryptor = AES.new(key, mode, IV=IV)

text = b'this is a test' # it must be a multiple of 16 byte (size of the basic AES block)
print(f"\n* Message: {text}")

"""

POSSIBLE FIX 

Switch from CBC (AES.MODE_CBC) to CFB (AES.MODE_CFB). With the default segment_size used by PyCrypto (pycryptodome for python3), you will not have any restriction on plaintext and ciphertext lengths.

Keep CBC and use a padding scheme like PKCS#7, that is:

    before encrypting a plaintext of X bytes, append to the back as many bytes you need to to reach the next 16 byte boundary. All padding bytes have the same value: the number of bytes that you are adding:

    length = 16 - (len(data) % 16) -> i love modulo
    data += bytes([length])*length

"""


enc_text = encryptor.encrypt(text)
print(f"\n* Encrypted message: {enc_text}")

decryptor = AES.new(key, mode, IV=IV)
plain = decryptor.decrypt(enc_text)
print(f"* Decrypted message: {plain}")
