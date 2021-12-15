import json

import Actor
import Director
import StreamingService

from database import IsolationLevel

class Media:

  def __init__(self, database, mediaData):
    self.database = database
    self.media_id = mediaData['media_id']
    self.data = mediaData

  def toDict(self):
    result = self.database.query('SELECT * FROM Media WHERE media_id = %s', (self.media_id, ))
    return dict(result[0])

  def getId(self):
    return self.media_id

  def getName(self):
    if 'name' in self.data:
      return self.data['name']
    result = self.database.query('SELECT name FROM Media WHERE media_id = %s', (self.media_id, ))
    self.data['name'] = result[0]['name']
    return self.data['name']

  def setName(self, name):
    self.database.execute('UPDATE Media SET name = %s WHERE media_id = %s', (name, self.media_id))

  def getReleaseYear(self):
    if 'releaseYear' in self.data:
      return self.data['releaseYear']
    result = self.database.query('SELECT releaseYear FROM Media WHERE media_id = %s', (self.media_id, ))
    self.data['releaseYear'] = result[0]['releaseYear']
    return self.data['releaseYear']

  def setReleaseYear(self, releaseYear):
    self.database.execute('UPDATE Media SET releaseYear = %s WHERE media_id = %s', (releaseYear, self.media_id))

  def getGenre(self):
    if 'genre' in self.data:
      return self.data['genre']
    if 'genre_id' not in self.data:
      result = self.database.query('SELECT genre_id FROM Media WHERE media_id = %s', (self.media_id, ))
      self.data['genre_id'] = result[0]['genre_id']
    self.data['genre'] = self.database.getGenre(self.data['genre_id'])
    return self.data['genre']

  def setGenre(self, genre):
    self.database.execute('UPDATE Media SET genre_id = %s WHERE media_id = %s', (genre.getId(), self.media_id))

  def getDirector(self):
    if 'director' in self.data:
      return self.data['director']
    if 'director_id' not in self.data:
      result = self.database.query('SELECT director_id FROM Media WHERE media_id = %s', (self.media_id, ))
      self.data['director_id'] = result[0]['director_id']
    self.data['director'] = self.database.getDirector(self.data['director_id'])
    return self.data['director']

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

  def getAverageRating(self):
    if 'averageRating' in self.data:
      return self.data['averageRating']
    result = self.database.query('SELECT AVG(score) AS rating FROM MediaRating WHERE media_id = %s', (self.media_id, ))
    self.data['averageRating'] = result[0]['rating']
    return self.data['averageRating']

  def getStarringActors(self):
    results = []
    actors = self.database.query('SELECT * FROM StarsIn NATURAL JOIN Actor WHERE media_id = %s', (self.media_id, ))
    for actorData in actors:
      results.append(Actor.Actor(self.database, actorData))
    return results

  def getNotStarringActors(self):
    results = []
    actors = self.database.query('SELECT * FROM Actor WHERE actor_id NOT IN (SELECT actor_id FROM StarsIn WHERE media_id = %s)', (self.media_id, ))
    for actorData in actors:
      results.append(Actor.Actor(self.database, actorData))
    return results

  def setStarredActors(self, actorList):
    self.database.beginTransaction(IsolationLevel.SERIALIZABLE)
    cursor = self.database.conn.cursor()
    try:
      cursor.execute('DELETE FROM StarsIn WHERE media_id = %s', (self.media_id, ))
      for actor in actorList:
        cursor.execute('INSERT INTO StarsIn(media_id, actor_id) VALUES (%s, %s)', (self.media_id, actor.getId()))
      cursor.close()
      self.database.commitTransaction()
    except:
      self.database.rollbackTransaction()

  def getAvailableStreamingServices(self):
    results = []
    services = self.database.query('SELECT * FROM ViewableOn NATURAL JOIN StreamingService WHERE media_id = %s', (self.media_id, ))
    for serviceData in services:
      results.append(StreamingService.StreamingService(self.database, serviceData))
    return results

  def getUnavailableStreamingServices(self):
    results = []
    services = self.database.query('SELECT * FROM StreamingService WHERE ss_id NOT IN (SELECT ss_id FROM ViewableOn WHERE media_id = %s)', (self.media_id, ))
    for serviceData in services:
      results.append(StreamingService.StreamingService(self.database, serviceData))
    return results

  def setAvailableStreamingServices(self, streamingServiceList):
    self.database.beginTransaction(IsolationLevel.SERIALIZABLE)
    cursor = self.database.conn.cursor()
    try:
      cursor.execute('DELETE FROM ViewableOn WHERE media_id = %s', (self.media_id, ))
      for streamingService in streamingServiceList:
        cursor.execute('INSERT INTO ViewableOn(media_id, ss_id) VALUES (%s, %s)', (self.media_id, streamingService.getId()))
      cursor.close()
      self.database.commitTransaction()
    except:
      self.database.rollbackTransaction()
