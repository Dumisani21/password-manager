import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class SecureEncryptor:
    def __init__(self, password, salt):
        self.password = password
        self.salt = salt
        self.key = self.generate_encryption_key()

    def generate_encryption_key(self):
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                iterations=100000,  # You can adjust the number of iterations for desired security
                salt=self.salt,
                length=32  # Length of the derived key
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.password.encode()))
            return key
        except Exception as e:
            print(f"Error generating encryption key: {e}")
            return None

    def encrypt(self, plaintext):
        try:
            fernet = Fernet(self.key)
            ciphertext = fernet.encrypt(plaintext.encode())
            return ciphertext
        except Exception as e:
            print(f"Encryption error: {e}")
            return None

    def decrypt(self, ciphertext):
        try:
            fernet = Fernet(self.key)
            plaintext = fernet.decrypt(ciphertext).decode()
            return plaintext
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

if __name__ == "__main__":
    salt = os.urandom(16)
    password = getpass.getpass("Enter your master password: ")
    encryptor = SecureEncryptor(password, salt)

    plaintext = "This is a secret message"
    ciphertext = encryptor.encrypt(plaintext)

    password = getpass.getpass("Enter your master password: ")
    encryptor = SecureEncryptor(password, salt)

    if ciphertext:
        print(f"Ciphertext: {ciphertext}")

        decrypted_text = encryptor.decrypt(ciphertext)
        if decrypted_text:
            print(f"Decrypted Text: {decrypted_text}")
