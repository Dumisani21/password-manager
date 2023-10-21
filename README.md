# password-manager

I am developing a password manager to assist in securely storing passwords on a local computer. With the increasing number of online accounts, it can be challenging to remember all passwords. The password manager requires only one master password to decrypt all stored passwords. This project is currently in progress and not yet complete. While there are many existing password managers, this one is my personal creation for enjoyment.

## Setup the program

```bash
# Run this command to install all requirements for this program to run
pip install -r requirements.txt
```

## Commands

```bash
# The following commands don't work yet
Commands:
  edit          Edit a user
  remove        Remove a user
```

```bash
# To create a vault
python main.py vault --name MyAcccounts 

# To list all vaults
python main.py list-vaults

┏━━━━━━━━━━━━┓
┃ Vaults     ┃
┡━━━━━━━━━━━━┩
│ MyAccounts │
└────────────┘

# To to save user details
python main.py create --username john@example.com --password john1234 --website youtube.com --vault MyAccounts
> Enter your master password: 
[+] Password created successfully!

# To list all passwords
python main.py list-psw --vault MyAccounts
┏━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ ID ┃ Username         ┃ Website     ┃ Password ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 1  │ john@example.com │ youtube.com │ ******** │
└────┴──────────────────┴─────────────┴──────────┘

# To list all passwords unmasked
python main.py list-psw --vault MyAccounts --unmask
> Enter your master password: 
┏━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ ID ┃ Username         ┃ Website     ┃ Password ┃
┡━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 1  │ john@example.com │ youtube.com │ john1234 │
└────┴──────────────────┴─────────────┴──────────┘


# To remove a vault
python main.py remove-vault --name MyAccounts
python main.py list-vaults
[-] No vaults found! 
```
