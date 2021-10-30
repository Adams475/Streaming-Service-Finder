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

  def createUser(self, username, hashedPassword):
    cursor = self.conn.cursor()
    cursor.execute('INSERT INTO User(username, hashedPassword) VALUES (?, ?)', (username, hashedPassword))
    user_id = cursor.lastrowid
    cursor.close()
    self.conn.commit()
    return self.getUser(user_id)

  def getMedia(self, media_id):
    result = self.conn.execute(f'SELECT COUNT(*) FROM Media WHERE media_id = {media_id}').fetchone()
    if result[0] == 0:
      return None
    return Media(self, media_id)

  def getAllStreamingServices(self):
    streamingServices = self.conn.execute('SELECT * FROM StreamingService')
    result = []
    for service in streamingServices:
      result.append(self.getStreamingService(service['ss_id']))
    return result

  def getAllGenres(self):
    genres = self.conn.execute('SELECT * FROM Genre')
    result = []
    for genre in genres:
      result.append(self.getGenre(genre['genre_id']))
    return result

  def getAllDirectors(self):
    directors = self.conn.execute('SELECT * FROM Director')
    result = []
    for director in directors:
      result.append(self.getDirector(director['director_id']))
    return result

  def getAllActors(self):
    actors = self.conn.execute('SELECT * FROM Actor')
    result = []
    for actor in actors:
      result.append(self.getActor(actor['actor_id']))
    return result

  def getAllUsers(self):
    users = self.conn.execute('SELECT * FROM User')
    result = []
    for user in users:
      result.append(self.getUser(user['user_id']))
    return result

  def getAllMedias(self):
    medias = self.conn.execute('SELECT * FROM Media')
    result = []
    for media in medias:
      result.append(self.getMedia(media['media_id']))
    return result

  def searchUserByUsername(self, username):
    result = self.conn.execute(f'SELECT user_id FROM User WHERE username = "{username}"').fetchone()
    if result is None:
      return None
    return User(self, result['user_id'])
