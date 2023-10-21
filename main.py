from cli_commands import *
from database import *
from base.base import Database
from rich import print
import click
# import bcrypt
import getpass
import hashlib
import os
import sys, getpass
import string, random
import cryptography.fernet as Fernet
from security.secure import *
from printTable import display


# Setup the database
# if not os.path.exists("database/psw_manager.db"):
#     database = Database("database/psw_manager.db")
#     database.create_table("users", "id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT")
database = Database("database/psw_manager.db")
HASHED_MASTER_PASSWORD = b'\x8b\x86\rlS\xd5b\x9eD\xb2D\x953LW\xb8\xaf\xa7.s\xe1\x1c`\xde\x03R\xc5|\x08\xbd\xef\xb9n\xf1\xaf\xcbp\xf5L\x92\xa7\x97u\x02#\xf6\x1bK'

# Verify the vault exists
def verify_vault_exists(vault_name):
    database_table = database.get_database_tables()
    if database_table is None or len(database_table) == 0:
        return False
    else:
        return vault_name in [table[0] for table in database_table]


# Verify the website exists
def verify_website_exists(website, vault_name):
    data = database.view_data(vault_name, 'website', f"website='{website}'")
    if data == None or len(data) == 0:
        return False
    elif data[0][0] == website:
        return True
    return False

def gen_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k = 18))

def verify_id_exists(id, vault_name):
    data = database.view_data(vault_name, 'id', f"id='{id}'")
    if data == None or len(data) == 0:
        return False
    elif data[0][0] == id:
        return True
    return False

# Command line functions

# Create a booking
@click.group()
def psw_manager():
    pass


@click.command(help='Create a new vault')
@click.option('--name','-n', help='Vault name', required=True)
def vault(name):
    """Create a new vault
    args: name"""
    name = name.strip()
    if name == "":
        print("[red][-] Vault name cannot be empty! [/red]")
        sys.exit()
    else:
        if verify_vault_exists(name):
            print("[red][-] Vault already exists! [/red]")
            sys.exit()
        database.create_table(name, 'id TEXT PRIMARY KEY, username TEXT, website TEXT, password TEXT, salt TEXT')
        print("[green][+] Vault created successfully! [/green]")

@click.command(help='List all vaults')
def list_vaults():
    database_table = list(filter(lambda column: column[0] != 'sqlite_sequence', database.get_database_tables()))

    if database_table == None or len(database_table) == 0:
        print("[red][-] No vaults found! [/red]")
    else:
        display(
            {
                "columns": ["Vaults"],
                "rows": [[table[0]] for table in database_table]
            }
        )

@click.command(help='Remove a vault')
@click.option('--name','-n', help='Vault name', required=True)
def remove_vault(name):
    name = name.strip()
    if name == "":
        print("[red][-] Vault name cannot be empty! [/red]")
        sys.exit()
    else:
        database.drop_table(name)

def empty_field(*fields):
    for field in fields:
        if field == "":
            return True
    return False

@click.command(help='Create a new user')
@click.option('--username','-u', help='Username', required=True)
@click.option('--password','-p', help='Password', required=True)
@click.option('--website','-w', help='Website', required=True)
@click.option('--vault','-v', help='Vault name', required=True)
def create(username, password, website, vault):
    username = username.strip()
    password = password.strip()
    website = website.strip()
    vault = vault.strip()
    print(username, password, website, vault)

    if empty_field(username, password, website, vault):
        print("[red][-] required input flied's cannot be empty! [/red]")
        sys.exit()
    else:
        if verify_vault_exists(vault):
            if verify_website_exists(website, vault):
                print("[red][-] Website already exists! [/red]")
                sys.exit()
            else:
                mp = getpass.getpass("Enter your master password: ")
                if verify_master_password(mp, HASHED_MASTER_PASSWORD):
                    salt = os.urandom(16)
                    encrypted_password = encrypt_and_store_key(mp, password, salt)
                    id = gen_id()
                    while verify_id_exists(id, vault):
                        id = gen_id()
                    database.insert_data(vault, (id, username, website, encrypted_password, salt))
                    print("[green][+] Password created successfully! [/green]")
                else:
                    print("[red][-] Master password is incorrect! [/red]")
                    sys.exit()
        else:
            print("[red][-] Vault does not exist! [/red]")
            sys.exit()


@click.command(help='List all vault passwords')
@click.option('--vault','-v', help='Vault name', required=True)
@click.option('--unmask','-u', help='Unmask passwords', is_flag=True, required=False, default=False)
def list_psw(vault, unmask=False):
    vault = vault.strip()
    if vault == "":
        print("[red][-] Vault name cannot be empty! [/red]")
        sys.exit()
    else:
        if verify_vault_exists(vault):
            data = database.view_data(vault, columns="oid, *")
            if data == None or len(data) == 0:
                print("[red][-] No passwords found! [/red]")
            else:
                if unmask:
                    mp = getpass.getpass("Enter your master password: ")
                    if verify_master_password(mp, HASHED_MASTER_PASSWORD):
                        data = [[str(row[0]), row[2], row[3], decrypt_key(mp, row[4], row[5])] for row in data]
                        display(
                            { 
                                "columns": ["ID", "Username", "Website", "Password"],
                                "rows": data
                            }
                        )
                    else:
                        print("[red][-] Master password is incorrect! [/red]")
                        sys.exit()
                else:
                    
                    # for row in data:
                    #     print(row[4])
                    data = [[str(row[0]), row[2], row[3], "********"] for row in data]
                    
                    display(
                        {
                            "columns": ["ID", "Username", "Website", "Password"],
                            "rows": data
                        }
                    )
        else:
            print("[red][-] Vault does not exist! [/red]")
            sys.exit()


@click.command(help='Remove a user')
def remove():
    pass

    
@click.command(help='Edit a user')
def edit(help='Edit a user'):
    pass


psw_manager.add_command(create)
psw_manager.add_command(remove)
psw_manager.add_command(edit)
psw_manager.add_command(vault)
psw_manager.add_command(remove_vault)
psw_manager.add_command(list_vaults)
psw_manager.add_command(list_psw)


if __name__ == '__main__':
    psw_manager()
    # if os.path.exists(os.path.join(getpass.getuser(), '.eagle_eye',"config.json")):
    #     psw_manager()
    # else:
    #     print("[red][-] Please run setup.py first! [/red]")
    #     sys.exit()
