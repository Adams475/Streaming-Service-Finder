import sqlite3

class Database:
	def __init__(self):
		self.conn = sqlite3.connect('streamfinder.sqlite3')
		self.conn.row_factory = sqlite3.Row
		self.conn.execute('PRAGMA foreign_keys = ON')
		self.conn.commit()

	### Sample getUsers method
	def getUsers(self):
		users = self.conn.execute('SELECT * FROM users').fetchall()
		return users


