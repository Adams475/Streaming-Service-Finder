import json

class StreamingService:

  def __init__(self, database, ss_id):
    self.database = database
    self.ss_id = ss_id

  def toDict(self):
    result = self.database.conn.execute(f'SELECT * FROM StreamingService WHERE ss_id = {self.ss_id}').fetchone()
    if result is None:
      return {}
    return dict(result)

  def getId(self):
    return self.ss_id

  def getName(self):
    result = self.database.conn.execute(f'SELECT name FROM StreamingService WHERE ss_id = {self.ss_id}').fetchone()
    return result['name']

  def setName(self, name):
    self.database.conn.execute(f'UPDATE StreamingService SET name = "{name}" WHERE ss_id = {self.ss_id}')
    self.database.conn.commit()

  def getCorrespondingMedia(self):
    medias = self.database.conn.execute(f'SELECT media_id FROM ViewableOn WHERE ss_id = {self.ss_id}')
    result = []
    for media in medias:
      result.append(self.database.getMedia(media['media_id']))
    return result

  def makeUnavailable(self, media):
    self.database.conn.execute(f'DELETE FROM ViewableOn WHERE ss_id = {self.ss_id} AND media_id = {media.getId()}')
    self.database.conn.commit()


