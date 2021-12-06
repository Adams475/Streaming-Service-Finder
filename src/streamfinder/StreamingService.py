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
    self.database.execute('UPDATE StreamingService SET name = %s WHERE ss_id = %s', (name, self.ss_id))

  def getCorrespondingMedia(self):
    medias = self.database.query('SELECT media_id FROM ViewableOn WHERE ss_id = %s', (self.ss_id, ))
    result = []
    for media in medias:
      result.append(self.database.getMedia(media['media_id']))
    return result

  def makeUnavailable(self, media):
    self.database.execute('DELETE FROM ViewableOn WHERE ss_id = %s AND media_id = %s', (self.ss_id, media.getId()))


