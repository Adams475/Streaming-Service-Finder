import json

class StreamingService:

  def __init__(self, database, ss_id):
    self.database = database
    self.ss_id = ss_id

  def toDict(self):
    result = self.database.query('SELECT * FROM StreamingService WHERE ss_id = %s', (self.ss_id, ))
    return dict(result[0])

  def getId(self):
    return self.ss_id

  def getName(self):
    result = self.database.query('SELECT name FROM StreamingService WHERE ss_id = %s', (self.ss_id, ))
    return result[0]['name']

  def setName(self, name):
    self.database.conn.execute(f'UPDATE StreamingService SET name = "{name}" WHERE ss_id = {self.ss_id}')
    self.database.conn.commit()

  def getCorrespondingMedia(self):
    medias = self.database.query('SELECT media_id FROM ViewableOn WHERE ss_id = %s', (self.ss_id, ))
    result = []
    for media in medias:
      result.append(self.database.getMedia(media['media_id']))
    return result

  def makeUnavailable(self, media):
    self.database.conn.execute(f'DELETE FROM ViewableOn WHERE ss_id = {self.ss_id} AND media_id = {media.getId()}')
    self.database.conn.commit()


