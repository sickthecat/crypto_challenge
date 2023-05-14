#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def aes_ecb_decrypt(key, encrypted_text):
    try:
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = base64.b64decode(encrypted_text)
        decrypted_data = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_data, AES.block_size).decode()
        return plaintext
    except (ValueError, KeyError) as e:
        # Handle decryption errors
        print("Decryption error:", str(e))
        return None


key = b'BA891CF4F992F85F44B3BF546E9B8F7C'  # 128-bit key note the b' indicates bytes (hex)
encrypted_text = "ZazIwL1QzSsbDflp45I1+uKn1kbXjjMLHZjNvmopX0c="  # Encrypted text result from plain-text!
decrypted_text = aes_ecb_decrypt(key, encrypted_text)
if decrypted_text is not None:
    print("Decrypted Text:", decrypted_text)
else: # Check Key or IV!
    print("Decryption failed.")
