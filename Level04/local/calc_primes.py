from sympy import primerange

# Generate 4-digit prime numbers
primes = list(primerange(1000, 10000))

# Print the generated prime numbers
for prime in primes:
    print(prime)
