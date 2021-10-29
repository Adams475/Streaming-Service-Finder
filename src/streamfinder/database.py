import sqlite3

from streamfinder.StreamingService import StreamingService
from streamfinder.Genre import Genre
from streamfinder.Director import Director
from streamfinder.Actor import Actor
from streamfinder.User import User
from streamfinder.Media import Media

class Database:
	def __init__(self):
		self.conn = sqlite3.connect('streamfinder.sqlite3')
		self.conn.row_factory = sqlite3.Row
		self.conn.execute('PRAGMA foreign_keys = ON')
		self.conn.commit()

	def getStreamingService(self, ss_id):
		result = self.conn.execute(f'SELECT COUNT(*) FROM StreamingService WHERE ss_id = {ss_id}').fetchone()
		if result[0] == 0:
			return None
		return StreamingService(self, ss_id)

	def getGenre(self, genre_id):
		result = self.conn.execute(f'SELECT COUNT(*) FROM Genre WHERE genre_id = {genre_id}').fetchone()
		if result[0] == 0:
			return None
		return Genre(self, genre_id)

	def getDirector(self, director_id):
		result = self.conn.execute(f'SELECT COUNT(*) FROM Director WHERE director_id = {director_id}').fetchone()
		if result[0] == 0:
			return None
		return Director(self, director_id)

	def getActor(self, actor_id):
		result = self.conn.execute(f'SELECT COUNT(*) FROM Actor WHERE actor_id = {actor_id}').fetchone()
		if result[0] == 0:
			return None
		return Actor(self, actor_id)

	def getUser(self, user_id):
		result = self.conn.execute(f'SELECT COUNT(*) FROM User WHERE user_id = {user_id}').fetchone()
		if result[0] == 0:
			return None
		return User(self, user_id)

	def getMedia(self, media_id):
		result = self.conn.execute(f'SELECT COUNT(*) FROM Media WHERE media_id = {media_id}').fetchone()
		if result[0] == 0:
			return None
		return Media(self, media_id)
