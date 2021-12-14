import json

import streamfinder.Media
from streamfinder.database import IsolationLevel

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

  def getAvailableMedia(self):
    medias = self.database.query('SELECT media_id FROM ViewableOn WHERE ss_id = %s', (self.ss_id, ))
    result = []
    for media in medias:
      result.append(self.database.getMedia(media['media_id']))
    return result

  def getUnavailableMedia(self):
    medias = []
    result = self.database.query('SELECT media_id FROM Media WHERE media_id NOT IN (SELECT media_id FROM ViewableOn WHERE ss_id = %s)', (self.ss_id, ))
    for media in result:
      medias.append(streamfinder.Media.Media(self.database, media['media_id']))
    return medias

  def setAvailableMedia(self, mediaList):
    self.database.beginTransaction(IsolationLevel.READ_COMMITTED)
    cursor = self.database.conn.cursor()
    try:
      cursor.execute('DELETE FROM ViewableOn WHERE ss_id = %s', (self.ss_id, ))
      for media in mediaList:
        cursor.execute('INSERT INTO ViewableOn(media_id, ss_id) VALUES (%s, %s)', (media.getId(), self.ss_id))
      cursor.close()
      self.database.commitTransaction()
    except:
      cursor.close()
      self.database.rollbackTransaction()

