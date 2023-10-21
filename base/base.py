import sqlite3

class Database:

	def __init__(self, db_name):
		try:
			self.conn = sqlite3.connect(db_name)
			self.c = self.conn.cursor()
			# print(f"Connected to database '{db_name}'")
		except sqlite3.Error as e:
			# print(f"Error connecting to database: {e}")
			return None

	def __del__(self):
		self.conn.close()

	def create_table(self, table_name, attributes):
		try:
			self.c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({attributes})")
			# print(f"Table '{table_name}' created successfully")
		except sqlite3.Error as e:
			print(f"Error creating table: {e}")
			return None

	def insert_data(self, table_name, data):
		try:
			placeholder = '?'
			placeholders = ', '.join(placeholder * len(data))
			
			self.c.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", data)
			self.conn.commit()
			# print(f"{self.c.rowcount} rows inserted successfully")
		except sqlite3.Error as e:
			# print(f"Error inserting data: {e}")
			return None

	def update_data(self, table_name, set_clause, where_clause):
		try:
			self.c.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}")
			self.conn.commit()
			# print(f"{self.c.rowcount} rows updated successfully")
		except sqlite3.Error as e:
			# print(f"Error updating data: {e}")
			return None

	def delete_data(self, table_name, where_clause):
		try:
			self.c.execute(f"DELETE FROM {table_name} WHERE {where_clause}")
			self.conn.commit()
			# print(f"{self.c.rowcount} rows deleted successfully")
		except sqlite3.Error as e:
			# (f"Error deleting data: {e}")
			return None

	def drop_table(self, table_name):
		try:
			self.c.execute(f"DROP TABLE IF EXISTS {table_name}")
			self.conn.commit()
			# print(f"Table '{table_name}' dropped successfully")
		except sqlite3.Error as e:
			# return(f"Error dropping table: {e}")
			return None

	def view_data(self, table_name, columns='*', where_clause=None):
		try:
			if where_clause:
				self.c.execute(f"SELECT {columns} FROM {table_name} WHERE {where_clause}")
			else:
				self.c.execute(f"SELECT {columns} FROM {table_name}")
			data = self.c.fetchall()
			# print(f"{len(data)} rows returned")
			return data
		except sqlite3.Error as e:
			# return(f"Error viewing data: {e}")
			return None

	def get_tables_names(self, table_name):
		try:
			self.c.execute(f"SELECT * FROM {table_name}")
			data = list(map(lambda x: x[0], self.c.description))
			return data
		except sqlite3.Error as e:
			# return (f"Error: {e}")
			return None
		

	def get_database_tables(self):
		try:
			self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
			data = self.c.fetchall()
			return data
		except sqlite3.Error as e:
			# return (f"Error: {e}")
			return None
		
	# execute sql script
	def execute_sql_script(self, script_file):
		try:
			# Read the SQL script from the file and execute it
			with open(script_file, "r") as sql_file:
				sql_script = sql_file.read().strip()
				self.c.executescript(sql_script)
				self.conn.commit()

			# print("SQL script executed successfully.")

		except sqlite3.Error as e:
			# print(f"Error executing SQL script: {str(e)}")
			return None