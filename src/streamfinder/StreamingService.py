import json

import streamfinder.Media
from streamfinder.database import IsolationLevel

class StreamingService:

  def __init__(self, database, ssData):
    self.database = database
    self.ss_id = ssData['ss_id']
    self.data = ssData

  def toDict(self):
    result = self.database.query('SELECT * FROM StreamingService WHERE ss_id = %s', (self.ss_id, ))
    return dict(result[0])

  def getId(self):
    return self.ss_id

  def getName(self):
    if 'name' in self.data:
      return self.data['name']
    result = self.database.query('SELECT name FROM StreamingService WHERE ss_id = %s', (self.ss_id, ))
    self.data['name'] = result[0]['name']
    return self.data['name']

  def setName(self, name):
    self.database.execute('UPDATE StreamingService SET name = %s WHERE ss_id = %s', (name, self.ss_id))

  def getAvailableMedia(self):
    results = []
    medias = self.database.query('SELECT * FROM ViewableOn NATURAL JOIN Media WHERE ss_id = %s', (self.ss_id, ))
    for mediaData in medias:
      results.append(streamfinder.Media.Media(self.database, mediaData))
    return results

  def getUnavailableMedia(self):
    results = []
    medias = self.database.query('SELECT * FROM Media WHERE media_id NOT IN (SELECT media_id FROM ViewableOn WHERE ss_id = %s)', (self.ss_id, ))
    for mediaData in medias:
      results.append(streamfinder.Media.Media(self.database, mediaData))
    return results

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

