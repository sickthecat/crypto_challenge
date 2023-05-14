#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def aes_ecb_encrypt(key, plaintext):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return base64.b64encode(ciphertext).decode()

# Usage example
key = b'BA891CF4F992F85F44B3BF546E9B8F7C'  # 128-bit key
plaintext = "BQCH-MKPADM-NN7F"
encrypted_text = aes_ecb_encrypt(key, plaintext)
print("Encrypted Text:", encrypted_text)
