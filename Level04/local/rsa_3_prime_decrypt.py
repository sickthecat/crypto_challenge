from math import gcd

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

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def decrypt_rsa(encrypted, primes):
    p, q, r = primes
    n = p * q * r
    e = 65537  # Public exponent
    phi = (p - 1) * (q - 1) * (r - 1)
    d = mod_inverse(e, phi)  # Private exponent
    decrypted = [chr(pow(char, d, n)) for char in encrypted]
    return "".join(decrypted)

def main():
    encrypted_message = input("Enter the encrypted message (space-separated): ")
    encrypted_message = [int(x) for x in encrypted_message.split()]

    try:
        primes = []

        for i in range(3):
            factor = int(input(f"Enter the prime factor {i+1}: "))
            if not is_prime(factor):
                raise ValueError(f"Factor {i+1} is not a prime number.")
            primes.append(factor)

            # Check if the prime factor is distinct
            if len(set(primes)) != i+1:
                raise ValueError("Prime factors must be distinct.")

        decrypted_message = decrypt_rsa(encrypted_message, primes)

        print("Decrypted message:")
        print(decrypted_message)

    except ValueError as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
