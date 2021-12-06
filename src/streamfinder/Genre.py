import json

from streamfinder.Media import Media

class Genre:

  def __init__(self, database, genre_id):
    self.database = database
    self.genre_id = genre_id

  def toDict(self):
    result = self.database.query('SELECT * FROM Genre WHERE genre_id = %s', (self.genre_id, ))
    return dict(result[0])

  def getId(self):
    return self.genre_id

  def getName(self):
    result = self.database.query('SELECT name FROM Genre WHERE genre_id = %s', (self.genre_id, ))
    return result[0]['name']

  def setName(self, name):
    self.database.conn.execute(f'UPDATE Genre SET name = "{name}" WHERE genre_id = {self.genre_id}')
    self.database.conn.commit()

  def getDescription(self):
    result = self.database.query('SELECT description FROM Genre WHERE genre_id = %s', (self.genre_id, ))
    return result[0]['description']

  def setDescription(self, description):
    self.database.conn.execute(f'UPDATE Genre SET description = "{description}" WHERE genre_id = {self.genre_id}')
    self.database.conn.commit()

  def getCorrespondingMedia(self):
    medias = self.database.query('SELECT media_id FROM Media WHERE genre_id = %s', (self.genre_id, ))
    result = []
    for media in medias:
      result.append(Media(self.database, media['media_id']))
    return result