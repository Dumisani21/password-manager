from database import *
from base.base import Database
from rich import print
import click
import os
import sys, getpass
import string, random
from security.secure import *
from printTable import display
import pyperclip


# Setup the database
# if not os.path.exists("database/psw_manager.db"):
#     database = Database("database/psw_manager.db")
#     database.create_table("users", "id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT")
database = Database("database/psw_manager.db")
HASHED_MASTER_PASSWORD = b"\xe5\xc30\xdcjcZ\x04\xad\xef_\x02\xa95v\xd4\xac\xd35\x81\x80\xac\x96*Nq\xee,\xbfm\x1e\x8f\xa4\x81\nR$\xbd\xe2'\xfb\x05iN\xc7I\xe1\x14"

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
    return data and data[0][0] == website


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def get_valid_index(length, message):
    while True:
        id_str = input(message).strip()
        if not is_int(id_str):
            print("[red][-] Please enter a valid integer! [/red]")
        elif int(id_str) > length:
            print("[red][-] Id out of range! [/red]")
        else:
            return int(id_str)

def empty_field(*fields):
    return any(field == "" for field in fields)

def gen_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k = 18))

def verify_id_exists(id_str, vault_name):
    data = database.view_data(vault_name, 'id', f"id='{id_str}'")
    return data and data[0][0] == id_str


# Create a booking
@click.group()
def psw_manager():
    pass


@click.command(help='Create a new vault')
@click.option('--name', '-n', help='Vault name', required=True)
def vault(name):
    name = name.strip()
    if not name:
        print("[red][-] Vault name cannot be empty! [/red]")
        sys.exit(1)
    if verify_vault_exists(name):
        print("[red][-] Vault already exists! [/red]")
        sys.exit(1)
    database.create_table(name, 'id TEXT PRIMARY KEY, username TEXT, website TEXT, password TEXT, salt TEXT')
    print("[green][+] Vault created successfully! [/green]")

@click.command(help='List all vaults')
def list_vaults():
    database_tables = list(filter(lambda column: column[0] != 'sqlite_sequence', database.get_database_tables()))
    if not database_tables:
        print("[red][-] No vaults found! [/red]")
    else:
        display({"columns": ["Vaults"], "rows": [[table[0]] for table in database_tables]})

@click.command(help='Remove a vault')
@click.option('--name', '-n', help='Vault name', required=True)
def remove_vault(name):
    name = name.strip()
    if not name:
        print("[red][-] Vault name cannot be empty! [/red]")
        sys.exit(1)
    database.drop_table(name)



@click.command(help='Create a new user')
@click.option('--username', '-u', help='Username', required=True)
@click.option('--website', '-w', help='Website', required=True)
@click.option('--vault', '-v', help='Vault name', required=True)
def create(username, website, vault):
    username = username.strip()
    website = website.strip()
    vault = vault.strip()

    if empty_field(username, website, vault):
        print("[red][-] Required input fields cannot be empty! [/red]")
        sys.exit(1)

    if not verify_vault_exists(vault):
        print("[red][-] Vault does not exist! [/red]")
        sys.exit(1)

    if verify_website_exists(website, vault):
        print("[red][-] Website already exists! [/red]")
        sys.exit(1)

    master_password = getpass.getpass("Enter your master password: ")
    if not verify_master_password(master_password, HASHED_MASTER_PASSWORD):
        print("[red][-] Master password is incorrect! [/red]")
        sys.exit(1)

    password = get_password()
    salt = os.urandom(16)
    encrypted_password = encrypt_and_store_key(master_password, password, salt)
    user_id = generate_unique_id(vault, verify_id_exists)
    database.insert_data(vault, (user_id, username, website, encrypted_password, salt))
    print("[green][+] Password created successfully! [/green]")

def get_password():
    while True:
        password = getpass.getpass("Enter your password: ")
        confirm = getpass.getpass("Confirm your password: ")
        if password == confirm:
            return password
        print("Please ensure your passwords match!")

def generate_unique_id(vault, verify_id_exists):
    user_id = gen_id()
    while verify_id_exists(user_id, vault):
        user_id = gen_id()
    return user_id



@click.command(help="List all vault passwords")
@click.option("--vault", "-v", help="Vault name", required=True)
@click.option("--copy", "-c", help="Copies password", is_flag=True, default=False)
def list_psw(vault, copy):
    """
    List all passwords in a vault.

    Args:
        vault (str): Name of the vault.
        copy (bool): Whether to copy the password to the clipboard.
    """
    vault = vault.strip()
    if not vault:
        click.secho("[-] Vault name cannot be empty!", fg="red")
        sys.exit(1)

    if not verify_vault_exists(vault):
        click.secho("[-] Vault does not exist!", fg="red")
        sys.exit(1)

    data = database.view_data(vault, columns="oid, *")
    if not data:
        click.secho("[-] No passwords found!", fg="red")
        return

    if copy:
        master_password = getpass.getpass("Enter your master password: ")
        if not verify_master_password(master_password, HASHED_MASTER_PASSWORD):
            click.secho("[-] Master password is incorrect!", fg="red")
            sys.exit(1)

        data = [
            [str(row[0]), row[2], row[3], decrypt_key(master_password, row[4], row[5])]
            for row in data
        ]

        index = get_valid_index(len(data), "Enter the id for the password to copy: ") - 1
        pyperclip.copy(data[index][3])
        click.secho("[+] Your password has been copied to your clipboard!", fg="green")
    else:
        data = [[str(row[0]), row[2], row[3], "********"] for row in data]
        display({"columns": ["ID", "Username", "Website", "Password"], "rows": data})



@click.command(help='Remove a user')
@click.option('--vault','-v', help='Vault name', required=True)
def remove(vault):
    vault = vault.strip()
    if vault == "":
        print("[red][-] Vault name cannot be empty! [/red]")
        sys.exit(1)

    if verify_vault_exists(vault):
        data = database.view_data(vault, columns="oid, *")
        if data == None or len(data) == 0:
            print("[red][-] No passwords found! [/red]")
        else:
            mp = getpass.getpass("Enter your master password: ")
            if verify_master_password(mp, HASHED_MASTER_PASSWORD):
                
                data = [[str(row[0]), row[2], row[3], "********"] for row in data]
                
                display({ "columns": ["ID", "Username", "Website", "Password"],
                        "rows": data })

                index: int = get_valid_index(len(data), "Enter the id for the password to delete: ")

                database.delete_data(vault, f"oid = {index}")
                print("[green][+] Data username deleted! [/green]")

                    
    
@click.command(help='Edit a user')
def edit(help='Edit a user'):
    pass

@click.command(help='Change master password')
def change_master_password(help='Edit a user'):
    pass


psw_manager.add_command(create)
psw_manager.add_command(remove)
psw_manager.add_command(edit)
psw_manager.add_command(vault)
psw_manager.add_command(remove_vault)
psw_manager.add_command(list_vaults)
psw_manager.add_command(list_psw)
psw_manager.add_command(change_master_password)


if __name__ == '__main__':
    psw_manager()
    # if os.path.exists(os.path.join(getpass.getuser(), '.eagle_eye',"config.json")):
    #     psw_manager()
    # else:
    #     print("[red][-] Please run setup.py first! [/red]")
    #     sys.exit()
