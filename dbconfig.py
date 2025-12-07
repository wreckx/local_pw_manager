import sqlite3

def dbconfig():
	db = sqlite3.connect('passwords.db')
	cursor = db.cursor()
 
	query = """
 				CREATE TABLE IF NOT EXISTS master_password (
				id INTEGER PRIMARY KEY,
				password TEXT NOT NULL
				); 
			"""
	cursor.execute(query)
 
	query = """
				CREATE TABLE IF NOT EXISTS passwords (
				id INTEGER PRIMARY KEY,
				website TEXT NOT NULL,
				username TEXT,
				email TEXT,
				password TEXT NOT NULL
				);
			"""
	cursor.execute(query)

	return db, cursor