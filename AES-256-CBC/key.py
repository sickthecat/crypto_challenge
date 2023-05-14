#!/usr/bin/env python3

import secrets

def generate_key():
    key = secrets.token_hex(32).upper()  # 256-bit key (32 bytes)
    return key

def generate_iv():
    iv = secrets.token_hex(16).upper()  # 128-bit IV (16 bytes)
    return iv

# Generate the 256-bit key
key = generate_key()
print("256-bit Key:", key)

# Generate the 128-bit IV
iv = generate_iv()
print("128-bit IV:", iv)
