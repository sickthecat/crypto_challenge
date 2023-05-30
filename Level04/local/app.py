# no security and bugs because local.
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from math import gcd
import urllib.parse

# Encryption and Decryption Functions

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

def powmod(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def decrypt_rsa(encrypted, primes):
    p, q, r = primes
    n = p * q * r
    e = 65537  # Public exponent
    phi = (p - 1) * (q - 1) * (r - 1)
    d = mod_inverse(e, phi)  # Private exponent
    decrypted = [powmod(char, d, n) for char in encrypted]
    decrypted = [chr(char) for char in decrypted]
    return "".join(decrypted)

# Request Handler

class MyRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path != '/':
            self.send_error(404, "File not found")
            return

        self._set_response()
        self.wfile.write(b'''
            <html>
            <body>
            <h1>RSA Decryption</h1>
            <form method="POST">
                <label for="encrypted">Encrypted Message:</label><br>
                <textarea name="encrypted" id="encrypted" rows="4" cols="50" required pattern="[^\x00-\x7F]+"></textarea><br>
                <label for="factor1">First Prime Factor:</label><br>
                <input type="number" name="factor1" id="factor1" required><br>
                <label for="factor2">Second Prime Factor:</label><br>
                <input type="number" name="factor2" id="factor2" required><br>
                <label for="factor3">Third Prime Factor:</label><br>
                <input type="number" name="factor3" id="factor3" required><br>
                <input type="submit" value="Decrypt">
            </form>
            </body>
            </html>
        ''')

    def do_POST(self):
        if self.path != '/':
            self.send_error(404, "File not found")
            return

        if self.command != 'POST':
            self.send_error(405, "Method not allowed")
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = urllib.parse.parse_qs(post_data)

        encrypted_message = [int(x) for x in params['encrypted'][0].split()]

        try:
            factor1 = int(params['factor1'][0])
            if not is_prime(factor1):
                raise ValueError("Factor 1 is not a prime number.")

            factor2 = int(params['factor2'][0])
            if not is_prime(factor2):
                raise ValueError("Factor 2 is not a prime number.")

            factor3 = int(params['factor3'][0])
            if not is_prime(factor3):
                raise ValueError("Factor 3 is not a prime number.")

            primes = [factor1, factor2, factor3]
            decrypted_message = decrypt_rsa(encrypted_message, primes)

            self._set_response()
            self.wfile.write(f'''
                <html>
                <body>
                <h1>Decrypted Message:</h1>
                <p>{decrypted_message}</p>
                </body>
                </html>
            '''.encode('utf-8'))

        except ValueError as e:
            self._set_response()
            error_message = str(e).encode('utf-8', 'ignore')  # Encode the exception message using UTF-8 and ignore invalid characters
            self.wfile.write(f'''
                <html>
                <body>
                <h1>Error: {error_message.decode('utf-8')}</h1>
                </body>
                </html>
            '''.encode('utf-8'))

        except Exception as e:
            self._set_response()
            error_message = str(e).encode('utf-8', 'ignore')  # Encode the exception message using UTF-8 and ignore invalid characters
            self.wfile.write(f'''
                <html>
                <body>
                <h1>Error: {error_message.decode('utf-8')}</h1>
                </body>
                </html>
            '''.encode('utf-8'))

# Server Initialization and Execution

def run_server():
    server_address = ('', 8000)
    httpd = ThreadingHTTPServer(server_address, MyRequestHandler)

    print('Starting server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
