from security.secure import encrypt_and_store_key, decrypt_key, APPLICATION_KEY
import getpass, os

# master_password = getpass.getpass("Enter your master password: ")
# salt, encrypted_key = encrypt_and_store_key(master_password, APPLICATION_KEY)
# print("salt:", salt)
# print("encrypted key:", encrypted_key)
# with open('./keys.key', 'wb') as f:
#     f.write(encrypted_key)
#     f.write(b'\n')
#     f.write(salt)
#     f.close()
if os.path.exists('./keys.key'):
    with open('./keys.key', 'rb') as f:
        encrypted_info = f.read().split(b'\n')
        encrypted_key = encrypted_info[0]
        salt = encrypted_info[1]
        f.close()
    master_password = getpass.getpass("Enter your master password: ")
    decrypted_key = decrypt_key(master_password, salt, encrypted_key)
    # print("decrypted key:", encrypted_key)
    # print("salt:", salt)
# decrypted_key = derive_encryption_key(master_password, salt)
print("decrypted key:", decrypted_key)