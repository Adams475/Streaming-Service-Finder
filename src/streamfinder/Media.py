import json

import streamfinder.Actor
import streamfinder.StreamingService

from streamfinder.database import IsolationLevel

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

  def getAverageRating(self):
    result = self.database.query('SELECT AVG(score) AS rating FROM MediaRating WHERE media_id = %s', (self.media_id, ))
    return result[0]['rating']

  def getStarringActors(self):
    actors = []
    results = self.database.query('SELECT actor_id FROM Actor WHERE actor_id IN (SELECT actor_id FROM StarsIn WHERE media_id = %s)', (self.media_id, ))
    for actor in results:
      actors.append(streamfinder.Actor.Actor(self.database, actor['actor_id']))
    return actors

  def getNotStarringActors(self):
    actors = []
    results = self.database.query('SELECT actor_id FROM Actor WHERE actor_id NOT IN (SELECT actor_id FROM StarsIn WHERE media_id = %s)', (self.media_id, ))
    for actor in results:
      actors.append(streamfinder.Actor.Actor(self.database, actor['actor_id']))
    return actors

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
    streamingServices = []
    results = self.database.query('SELECT ss_id FROM StreamingService WHERE ss_id IN (SELECT ss_id FROM ViewableOn WHERE media_id = %s)', (self.media_id, ))
    for streamingService in results:
      streamingServices.append(streamfinder.StreamingService.StreamingService(self.database, streamingService['ss_id']))
    return streamingServices

  def getUnavailableStreamingServices(self):
    streamingServices = []
    results = self.database.query('SELECT ss_id FROM StreamingService WHERE ss_id NOT IN (SELECT ss_id FROM ViewableOn WHERE media_id = %s)', (self.media_id, ))
    for streamingService in results:
      streamingServices.append(streamfinder.StreamingService.StreamingService(self.database, streamingService['ss_id']))
    return streamingServices

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
