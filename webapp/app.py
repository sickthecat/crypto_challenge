from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
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
            "<input type='text' id='key' name='key' required><br>\n"
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
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        # Parse the form data
        data = parse_qs(body.decode())
        ciphertext = data['ciphertext'][0]
        key = bytes.fromhex(data['key'][0])
        iv = bytes.fromhex(data['iv'][0])

        if len(key) != 32:
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

        if len(iv) != 16:
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
            decrypted_text = decrypt_text(ciphertext, key, iv)
            response = (
                "<html>\n"
                "<head>\n"
                "<title>Message Decryption</title>\n"
                "</head>\n"
                "<body>\n"
                "<h1>Message Decryption</h1>\n"
                f"<p>Decrypted Text: {decrypted_text}</p>\n"
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
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
