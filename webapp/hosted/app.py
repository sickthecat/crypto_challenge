from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import string
import ssl


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(404, "Not Found")
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # HTML form for decryption input
        form = (
            "<html>\n"
            "<head>\n"
            "<title>Message Decryption</title>\n"
            "</head>\n"
            "<body>\n"
            "<h1>Message Decryption</h1>\n"
            "<form method='POST'>\n"
            "<label for='ciphertext'>Ciphertext:</label>\n"
            "<br>\n"
            "<input type='text' id='ciphertext' name='ciphertext' required><br>\n"
            "<label for='key'>Key:</label>\n"
            "<br>"
            "<input type='password' id='key' name='key' required><br>\n"
            "<label for='iv'>IV:</label>\n"
            "</br>\n"
            "<input type='text' id='iv' name='iv' required><br>\n"
            "<br>"
            "<input type='submit' value='Decrypt'>\n"
            "</form>\n"
            "</body>\n"
            "</html>\n"
        )

        self.wfile.write(form.encode())

    def do_POST(self):
        if self.path != '/':
            self.send_error(404, "Not Found")
            return

        if self.headers.get('Content-Type') != 'application/x-www-form-urlencoded':
            self.send_error(400, "Bad Request: Invalid Content-Type")
            return

        if self.command != 'POST':
            self.send_error(405, "Method Not Allowed")
            return

        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_error(400, "Bad Request: Empty body")
            return

        body = self.rfile.read(content_length)

        # Parse the form data
        try:
            data = parse_qs(body.decode(), strict_parsing=True)
        except ValueError:
            self.send_error(400, "Bad Request: Malformed data")
            return

        ciphertext = data.get('ciphertext', [''])[0]
        key = data.get('key', [''])[0]
        iv = data.get('iv', [''])[0]

        if not all(char in string.printable for char in ciphertext):
            self.send_error(400, "Bad Request: Ciphertext contains non-ASCII characters.")
            return

        if not all(char in string.printable for char in key):
            self.send_error(400, "Bad Request: Key contains non-ASCII characters.")
            return

        if not all(char in string.printable for char in iv):
            self.send_error(400, "Bad Request: IV contains non-ASCII characters.")
            return

        try:
            key_bytes = bytes.fromhex(key)
        except ValueError:
            self.send_error(400, "Bad Request: Invalid key format. Key must be in hexadecimal.")
            return

        if len(key_bytes) != 32:
            error_message = "Invalid key length. Key must be 32 bytes (256 bits)."
            response = (
                "<html>\n"
                "<head>\n"
                "<title>Message Decryption</title>\n"
                "</head>\n"
                "<body>\n"
                "<h1>Message Decryption</h1>\n"
                f"<p>Error occurred during decryption: {error_message}</p>\n"
                "</body>\n"
                "</html>\n"
            )
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode())
            return

        try:
            iv_bytes = bytes.fromhex(iv)
        except ValueError:
            self.send_error(400, "Bad Request: Invalid IV format. IV must be in hexadecimal.")
            return

        if len(iv_bytes) != 16:
            error_message = "Invalid IV length. IV must be 16 bytes (128 bits)."
            response = (
                "<html>\n"
                "<head>\n"
                "<title>Message Decryption</title>\n"
                "</head>\n"
                "<body>\n"
                "<h1>Message Decryption</h1>\n"
                f"<p>Error occurred during decryption: {error_message}</p>\n"
                "</body>\n"
                "</html>\n"
            )
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode())
            return

        try:
            decrypted_text = decrypt_text(ciphertext, key_bytes, iv_bytes)
            response = (
                "<html>\n"
                "<head>\n"
                "<title>Message Decryption</title>\n"
                "</head>\n"
                "<body>\n"
                "<h1>Message Decryption</h1>\n"
                f"<p>Decrypted Text: {decrypted_text}</p>\n Please email 5570706572456368656C6F6E[@]gmail.com to join the VIP club ;) ! Congratulations!"
                "</body>\n"
                "</html>\n"
            )
        except Exception as e:
            error_message = "Decryption error. Please check the key, IV, and ciphertext."
            response = (
                "<html>\n"
                "<head>\n"
                "<title>Message Decryption</title>\n"
                "</head>\n"
                "<body>\n"
                "<h1>Message Decryption</h1>\n"
                f"<p>Error occurred during decryption: {error_message}</p>\n"
                f"<p>{str(e)}</p>\n"
                "</body>\n"
                "</html>\n"
            )

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode())


def decrypt_text(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = base64.b64decode(ciphertext)
    decrypted_text = cipher.decrypt(ciphertext)
    return unpad(decrypted_text, AES.block_size).decode()


def run_server(server_class=ThreadingHTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    # Configure SSL/TLS
    cert_file = 'fullchain.pem'
    key_file = 'privkey.pem'
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    # Start the server with SSL/TLS
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    print(f'Starting server on port {port} with SSL/TLS...')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
