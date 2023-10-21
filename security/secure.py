import hashlib
import cryptography.fernet as Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from security.lock_master import SecureEncryptor
import os

# Generate a random encryption key for the application (once, during setup)


# Encrypt and store the encryption key (use the application key)
def encrypt_and_store_key(master_password, password, salt):
    encryption = SecureEncryptor(master_password, salt)
    encrypted = encryption.encrypt(password)
    return encrypted
    
 

# Decrypt the encryption key (use the application key)
def decrypt_key(master_password, encrypted_password, salt):
    encryption = SecureEncryptor(master_password, salt)
    decrypted = encryption.decrypt(encrypted_password)
    return decrypted
 

# Hash the master password using PBKDF2
def hash_master_password(master_password):
    salt = os.urandom(16)  # Generate a random salt
    key = hashlib.pbkdf2_hmac('sha256', master_password.encode('utf-8'), salt, 100000)
    return salt + key

# Verify the master password
def verify_master_password(master_password, stored_hash):
    salt = stored_hash[:16]
    key_to_check = hashlib.pbkdf2_hmac('sha256', master_password.encode('utf-8'), salt, 100000)
    return stored_hash == salt + key_to_check

if __name__ == '__main__':
    salt = os.urandom(16)
    master_password = "password"
    password = "password123123"

    encrypted = encrypt_and_store_key(master_password, password, salt)
    print(encrypted)
    decrypted = decrypt_key(master_password, salt, encrypted)
    print(decrypted)
