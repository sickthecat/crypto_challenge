#!/usr/bin/env python3

from Crypto.Random import get_random_bytes

# Generate a single 16-byte (128-bit) key
key = get_random_bytes(16)

# Convert the key to uppercase hexadecimal format
key_hex = key.hex().upper()

# Print the key
print("Key:", key_hex)
