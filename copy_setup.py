from rich import print
import getpass, os
import json
from security.secure import hash_master_password
from base.base import Database

# Variables
LOCATION = os.path.join(os.path.expanduser('~'), '.eagle_eye')
# print(LOCATION)
database_path = ""

def create_database(location):
    global database_path
    database_path = os.path.join(location, "database/psw_manager.db")
    if not os.path.exists(os.path.join(location, 'database')):
        os.mkdir(os.path.join(location,'database'))

    # Implement logic for creating the database here (using a library like sqlite3)
    Database(database_path)




def setup_master_password():
    message = """Minimum length: 12 characters (recommended)
Character types: Include a combination of uppercase letters, lowercase letters, numbers, and symbols."""
    while True:
        print("[green]Enter your master password: [/green]", end="")
        MASTER_PASSWORD = getpass.getpass("")
        if MASTER_PASSWORD == "":
            print("[red][-] Master password cannot be empty! [/red]")
        elif not check_password_strength(MASTER_PASSWORD):  # Implement password strength check
            print("[red] Please choose a stronger password![/red]")
            print(message)
        else:
            print("[green]Confirm your master password: [/green]", end="")
            CONFIRM_PASSWORD = getpass.getpass("")
            if MASTER_PASSWORD != CONFIRM_PASSWORD:
                print("[red] Passwords do not match! Try again. [/red]")
            else:
                hashed_password = hash_master_password(MASTER_PASSWORD)
                with open(os.path.join(LOCATION, "config.json"), "w") as f:
                    json.dump({"master_password": hashed_password.decode('utf-8', errors='ignore'),
                               "db_location": database_path
                               }, f)
                print("[green]Master password saved![/green]")
                return


def check_password_strength(password):
  """
  Checks the strength of a password based on length and character types.

  Args:
      password: The password to be checked.

  Returns:
      True if the password is strong, False otherwise.
  """
  minimum_length = 12  # Set a minimum password length
  has_uppercase = any(char.isupper() for char in password)
  has_lowercase = any(char.islower() for char in password)
  has_number = any(char.isdigit() for char in password)
  has_symbol = any(char in "!@#$%^&*()_+-=[]{};':|\,.<>/?`~" for char in password)

  # Check if all complexity requirements are met
  return (
      len(password) >= minimum_length and
      has_uppercase and
      has_lowercase and
      has_number and
      has_symbol
  )



def main():
    if not os.path.exists(LOCATION):
        os.makedirs(LOCATION)

        # Database creation logic (check if DB exists and handle appropriately)
        if not os.path.exists(os.path.join(LOCATION, "database")):
            create_database(LOCATION)
    else:
        print("[yellow] A configuration already exists. Data might be overwritten![/yellow]")

    setup_master_password()

    print("[green]Password Manager setup complete![/green]")


if __name__ == "__main__":
    main()
