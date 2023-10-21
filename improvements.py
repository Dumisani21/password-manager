import click
import os
import sys
import string
import random
import hashlib
import getpass
from base.base import Database

# Define the database filename
DATABASE_FILENAME = "database/psw_manager.db"

# Initialize the database
if not os.path.exists(DATABASE_FILENAME):
    database = Database(DATABASE_FILENAME)
    database.create_table("users", "id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT")
database = Database(DATABASE_FILENAME)

# Verify the vault exists
def verify_vault_exists(vault_name):
    database_table = database.get_database_tables()
    if database_table is None or len(database_table) == 0:
        return False
    else:
        return vault_name in [table[0] for table in database_table]

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

# ... (Other utility functions)

# Create a new user
@click.command(help='Create a new user')
@click.option('--username', '-u', help='Username', required=True)
@click.option('--password', '-p', help='Password', required=True)
@click.option('--website', '-w', help='Website', required=True)
@click.option('--vault', '-v', help='Vault name', required=True)
def create(username, password, website, vault):
    username = username.strip()
    password = password.strip()
    website = website.strip()
    vault = vault.strip()

    if not (username and password and website and vault):
        print("[red][-] Required input fields cannot be empty! [/red]")
        sys.exit()
    else:
        if verify_vault_exists(vault):
            if verify_website_exists(website, vault):
                print("[red][-] Website already exists! [/red]")
                sys.exit()
            else:
                hashed_password = hash_master_password(password)
                id = gen_id()
                while verify_id_exists(id, vault):
                    id = gen_id()
                database.insert_data(vault, (id, website, username, hashed_password))

# ... (Other commands)

if __name__ == '__main__':
    psw_manager()



# other improvements
import cryptography.fernet as Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Derive encryption key from master password using PBKDF2
def derive_encryption_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # Adjust the number of iterations as needed
        salt=salt,
        length=32  # Length of the key
    )
    key = Fernet.Fernet.generate_key()
    return key

# Encrypt and store the encryption key
def encrypt_and_store_key(master_password, key):
    salt = os.urandom(16)  # Generate a random salt
    encryption_key = derive_encryption_key(master_password, salt)
    fernet = Fernet.Fernet(encryption_key)
    encrypted_key = fernet.encrypt(key.encode('utf-8'))
    
    # Store salt and encrypted_key securely, e.g., in a configuration file
    return salt, encrypted_key

# Decrypt the encryption key
def decrypt_key(master_password, salt, encrypted_key):
    encryption_key = derive_encryption_key(master_password, salt)
    fernet = Fernet.Fernet(encryption_key)
    key = fernet.decrypt(encrypted_key)
    return key.decode('utf-8')

