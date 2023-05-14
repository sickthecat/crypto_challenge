#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def decrypt_text(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = base64.b64decode(ciphertext)
    decrypted_text = cipher.decrypt(ciphertext)
    return unpad(decrypted_text, AES.block_size).decode()

# Hardcoded ciphertext, key, and IV
ciphertext = "0mTCer3lrcwtMyf4AysTuOHe9ngD43P+8jiIsbcX52U="
key = bytes.fromhex('76AB7CADC042E18917F08BE4734A0D1BF378FAA025BC380A734B3AC080A48EC3')  # Convert key to bytes, 256 bit Key
iv = bytes.fromhex('56EC429BA8896D194E8FABA7C5EA4761')  # Convert IV to bytes, 128 bit Key

try:
    decrypted_text = decrypt_text(ciphertext, key, iv)
    print("Decrypted Text:", decrypted_text)
except Exception as e: #If this occurs, the IV or Key is wrong.
    print("Error occurred during decryption:", str(e))
