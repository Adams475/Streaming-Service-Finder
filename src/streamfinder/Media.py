import json

class Media:

  def __init__(self, database, media_id):
    self.database = database
    self.media_id = media_id

  def toDict(self):
    result = self.database.query('SELECT * FROM Media WHERE media_id = %s', (self.media_id, ))
    return dict(result[0])

  def getId(self):
    return self.media_id

  def getName(self):
    result = self.database.query('SELECT name FROM Media WHERE media_id = %s', (self.media_id, ))
    return result[0]['name']

  def setName(self, name):
    self.database.execute('UPDATE Media SET name = %s WHERE media_id = %s', (name, self.media_id))

  def getReleaseYear(self):
    result = self.database.query('SELECT releaseYear FROM Media WHERE media_id = %s', (self.media_id, ))
    return result[0]['releaseYear']

  def setReleaseYear(self, releaseYear):
    self.database.execute('UPDATE Media SET releaseYear = %s WHERE media_id = %s', (releaseYear, self.media_id))

  def getGenre(self):
    result = self.database.query('SELECT genre_id FROM Media WHERE media_id = %s', (self.media_id, ))
    return self.database.getGenre(result[0]['genre_id'])

  def setGenre(self, genre):
    self.database.execute('UPDATE Media SET genre_id = %s WHERE media_id = %s', (genre.getId(), self.media_id))

  def getDirector(self):
    result = self.database.query('SELECT director_id FROM Media WHERE media_id = %s', (self.media_id, ))
    return self.database.getDirector(result[0]['director_id'])

  def setDirector(self, director):
    self.database.execute('UPDATE Media SET director_id = %s WHERE media_id = %s', (director.getId(), self.media_id))

  def addRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.execute('INSERT INTO MediaRating(media_id, user_id, score) VALUES (%s, %s, %s)', (self.media_id, userID, score))

  def updateRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.execute('UPDATE MediaRating SET score = %s WHERE media_id = %s AND user_id = %s', (score, self.media_id, userID))

  def deleteRating(self, userID):
    self.database.execute('DELETE FROM MediaRating WHERE media_id = %s AND user_id = %s', (self.media_id, userID))