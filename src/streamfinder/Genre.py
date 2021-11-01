import json

class Genre:

  def __init__(self, database, genre_id):
    self.database = database
    self.genre_id = genre_id

  def toDict(self):
    result = self.database.conn.execute(f'SELECT * FROM Genre WHERE genre_id = {self.genre_id}').fetchone()
    if result is None:
      return {}
    return dict(result)

  def getId(self):
    return self.genre_id

  def getName(self):
    result = self.database.conn.execute(f'SELECT name FROM Genre WHERE genre_id = {self.genre_id}').fetchone()
    return result['name']

  def setName(self, name):
    self.database.conn.execute(f'UPDATE Genre SET name = "{name}" WHERE genre_id = {self.genre_id}')
    self.database.conn.commit()

  def getDescription(self):
    result = self.database.conn.execute(f'SELECT description FROM Genre WHERE genre_id = {self.genre_id}').fetchone()
    return result['description']

  def setDescription(self, description):
    self.database.conn.execute(f'UPDATE Genre SET description = "{description}" WHERE genre_id = {self.genre_id}')
    self.database.conn.commit()

  def getCorrespondingMedia(self):
    medias = self.database.conn.execute(f'SELECT * FROM Media WHERE genre_id = {self.genre_id}')
    result = []
    for media in medias:
      result.append(self.database.getMedia(media['media_id']))
    return result