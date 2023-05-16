# Challenge Repository

Welcome to the Challenge Repository! In this repository, you can participate in our challenge and decrypt the gift card code using various methods. You have three options to get started:  ``https://www.youtube.com/@UpperEchelon``

1. Emulate the Environment Locally (Linux):
   - Ensure that you have Python 3 and pip 3 installed on your Linux computer.
   - Install the following packages using pip:
     - `pycryptodome`
     - `cryptography`
   - Once the dependencies are installed, you can run the `decrypt.py` Python code locally.

2. Use a VPS (Virtual Private Server):
   - Set up a VPS environment of your choice.
   - Follow the instructions for emulating the environment locally mentioned above.
   - Run the `decrypt.py` Python code on your VPS.

3. Use the Pyodide Web Console:
   - Visit [https://pyodide.org/en/stable/console.html](https://pyodide.org/en/stable/console.html) in your web browser.
   - Edit the script with your puzzle findings.
   - Replace the appropriate fillers in the code snippet below with your values:
     ```python
     from Crypto.Cipher import AES
     from Crypto.Util.Padding import unpad
     import base64

     def decrypt_text(ciphertext, key, iv):
         cipher = AES.new(key, AES.MODE_CBC, iv)
         ciphertext = base64.b64decode(ciphertext)
         decrypted_text = cipher.decrypt(ciphertext)
         return unpad(decrypted_text, AES.block_size).decode()

     # Hardcoded ciphertext, key, and IV
     ciphertext = "0mTCer3lrcwtMyf4AysTuOHe9ngD43P+8jiIsbcX52U="  # change this! Find it!
     key = bytes.fromhex('76AB7CADC042E18917F08BE4734A0D1BF378FAA025BC380A734B3AC080A48EC3')  # Convert key to bytes, 256 bit Key! find it!
     iv = bytes.fromhex('56EC429BA8896D194E8FABA7C5EA4761')  # Convert IV to bytes, 128 bit Key! Find it.

     try:
         decrypted_text = decrypt_text(ciphertext, key, iv)
         print("Decrypted Text:", decrypted_text)
     except Exception as e:  # If this occurs, the IV or Key is wrong.
         print("Error occurred during decryption:", str(e))
     ```
   - Paste the modified code into the Pyodide console.
   - Press Enter twice to run the code and see the decrypted text.

Additionally, we provide a hosted web app for those who prefer a more comfortable experience. The chosen encryption method used is AES-256-CBC. To decrypt the gift card code, you'll need the following parts:
- http://afflicted.sh:8000/
- Encrypted message (ciphertext)
- 256-bit key
- 128-bit IV (Initialization Vector)

We encourage participants to learn more about encryption and its impact on privacy. Happy decrypting!

## Resources

If you're new to encryption or want to enhance your knowledge, here are some resources you might find helpful:

- [Introduction to Encryption](https://en.wikipedia.org/wiki/Encryption)
- [AES (Advanced Encryption Standard)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [Cryptography in Python](https://cryptography.io/en/latest/)
- [Pyodide Documentation](https://pyodide.org/)

Feel free to explore these resources to gain a deeper understanding of encryption principles and techniques. Good luck with the challenge!
