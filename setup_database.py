from base.base import Database
import os

# Setup the database
database = Database("database/psw_manager.db")

# Create vault table with password
database.create_table("vault", "id INTEGER PRIMARY KEY AUTOINCREMENT, password TEXT")