import json

class Media:

  def __init__(self, database, media_id):
    self.database = database
    self.media_id = media_id

  def toDict(self):
    result = self.database.conn.execute(f'SELECT * FROM Media WHERE media_id = {self.media_id}').fetchone()
    if result is None:
      return {}
    return dict(result)

  def getId(self):
    return self.media_id

  def getName(self):
    result = self.database.conn.execute(f'SELECT name FROM Media WHERE media_id = {self.media_id}').fetchone()
    return result['name']

  def setName(self, name):
    self.database.conn.execute(f'UPDATE Media SET name = "{name}" WHERE media_id = {self.media_id}')
    self.database.conn.commit()

  def getReleaseYear(self):
    result = self.database.conn.execute(f'SELECT releaseYear FROM Media WHERE media_id = {self.media_id}').fetchone()
    return result['releaseYear']

  def setReleaseYear(self, releaseYear):
    self.database.conn.execute(f'UPDATE Media SET releaseYear = {releaseYear} WHERE media_id = {self.media_id}')
    self.database.conn.commit()

  def getGenre(self):
    result = self.database.conn.execute(f'SELECT genre_id FROM Media WHERE media_id = {self.media_id}').fetchone()
    return self.database.getGenre(result['genre_id'])

  def setGenre(self, genre):
    self.database.conn.execute(f'UPDATE Media SET genre_id = {genre.getId()} WHERE media_id = {self.media_id}')
    self.database.conn.commit()

  def getDirector(self):
    result = self.database.conn.execute(f'SELECT director_id FROM Media WHERE media_id = {self.media_id}').fetchone()
    return self.database.getDirector(result['director_id'])

  def setDirector(self, director):
    self.database.conn.execute(f'UPDATE Media SET director_id = {director.getId()} WHERE media_id = {self.media_id}')
    self.database.conn.commit()

  def addRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.conn.execute(f'INSERT INTO MediaRating(media_id, user_id, score) VALUES ({self.getId()}, {userID}, {score})')
    self.database.conn.commit()

  def updateRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.conn.execute(f'UPDATE MediaRating SET score = {score} WHERE media_id = {self.getId()} AND user_id = {userID}')
    self.database.conn.commit()

  def deleteRating(self, userID):
    self.database.conn.execute(f'DELETE FROM MediaRating WHERE media_id = {self.getId()} AND user_id = {userID}')
    self.database.conn.commit()