import random
from math import gcd
from sympy import primerange

def mod_inverse(a, m):
    if gcd(a, m) != 1:
        raise ValueError("Modular inverse does not exist.")
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1,
            u2 - q * v2,
            u3 - q * v3,
            v1,
            v2,
            v3,
        )

    return u1 % m

def generate_rsa_primes():
    primes = random.sample(list(primerange(1000, 10000)), 3)  # Generate 3 random large primes
    return primes

def factorize_primes(primes):
    p, q, r = primes
    phi = (p - 1) * (q - 1) * (r - 1)
    e = 65537  # Public exponent
    d = mod_inverse(e, phi)  # Private exponent
    return d

def encrypt_rsa(message, primes):
    p, q, r = primes
    n = p * q * r
    e = 65537  # Public exponent
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted

def main():
    message = input("Enter the message to encrypt: ")
    primes = generate_rsa_primes()
    encrypted_message = encrypt_rsa(message, primes)

    print("Primes used for encryption:")
    print(primes)

    print("Encrypted message:")
    print(" ".join(map(str, encrypted_message)))

    factor1 = int(input("Enter the first prime factor: "))
    factor2 = int(input("Enter the second prime factor: "))
    factor3 = int(input("Enter the third prime factor: "))

    primes = [factor1, factor2, factor3]
    private_exponent = factorize_primes(primes)

    print("Private exponent (d):", private_exponent)

if __name__ == "__main__":
    main()
