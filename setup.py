from security.secure import *
from rich import print
from base.base import Database
import getpass, os
import json


# Variables
LOCATION = os.path.join(getpass.getuser(), '.eagle_eye')
base = Database(os.path.join(LOCATION, "database/psw_manager.db"))

def setupDatabase():
    base.execute_sql_script("database/setup_data.sql")

# Initialize the database
if not os.path.exists(os.path.join(LOCATION, "database")):
    setupDatabase()
else:
    # If exists, delete it
    os.removedirs(os.path.join(LOCATION, "database"))
    setupDatabase()


print("[bold][green]Welcome to the Password Manager![/green][/bold]")
print("[green] We will need a few details to setup your password. [/green]")

# Begin setup
if not os.path.exists(LOCATION):
    os.makedirs(LOCATION)
else:
    os.removedirs(LOCATION)

while True:
    MASTER_PASSWORD = ""

    print("[green]Enter your master password: [/green]", end="")
    MASTER_PASSWORD = getpass.getpass("")
    if MASTER_PASSWORD == "":
        print("[red][-] Master password cannot be empty! [/red]")
    else:
        print("[green]Master password set![/green]")
        hashed_password = hash_master_password(MASTER_PASSWORD)
        with open(os.path.join(LOCATION, "config.json"), "w") as f:
            json.dump({"master_password": hashed_password.decode('utf-8')}, f)
        print("[green]Master password saved![/green]")

        # Run the setup of database
        print("[green]Setting up database...[/green]")
        if not os.path.exists(os.path.join(LOCATION, "database")):
            pass
        break