#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

def encrypt_text(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()

# Hardcoded plaintext, key, and IV
plaintext = "BQCH-MKPADM-NN7F"
key = bytes.fromhex('76AB7CADC042E18917F08BE4734A0D1BF378FAA025BC380A734B3AC080A48EC3')  # Convert key to bytes
iv = bytes.fromhex('56EC429BA8896D194E8FABA7C5EA4761')  # Convert IV to bytes

try:
    encrypted_text = encrypt_text(plaintext, key, iv)
    print("Encrypted Text:", encrypted_text)
except Exception as e: #The Key or IV has not been input correctly, check that it's bytes...
    print("Error occurred during encryption:", str(e))
