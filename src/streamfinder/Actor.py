import streamfinder.Media
import streamfinder.database

class Actor:

  def __init__(self, database, actorData):
    self.database = database
    self.actor_id = actorData['actor_id']
    self.data = actorData

  def toDict(self):
    result = self.database.query('SELECT * FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    return dict(result[0])

  def getId(self):
    return self.actor_id

  def getName(self):
    if 'name' in self.data:
      return self.data['name']
    result = self.database.query('SELECT name FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    self.data['name'] = result[0]['name']
    return self.data['name']

  def setName(self, name):
    self.database.execute('UPDATE Actor SET name = %s WHERE actor_id = %s', (name, self.actor_id))

  def getSex(self):
    if 'sex' in self.data:
      return self.data['sex']
    result = self.database.query('SELECT sex FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    self.data['sex'] = result[0]['sex']
    return self.data['sex']

  def setSex(self, sex):
    self.database.execute('UPDATE Actor SET sex = %s WHERE actor_id = %s', (sex, self.actor_id))

  def getBirthDate(self):
    if 'birthDate' in self.data:
      return self.data['birthDate']
    result = self.database.query('SELECT birthDate FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    self.data['birthDate'] = result[0]['birthDate']
    return self.data['birthDate']

  def setBirthDate(self, birthDate):
    self.database.execute('UPDATE Actor SET birthDate = %s WHERE actor_id = %s', (birthDate, self.actor_id))

  def getStarredMedias(self):
    results = []
    medias = self.database.query('SELECT * FROM StarsIn NATURAL JOIN Media WHERE actor_id = %s', (self.actor_id, ))
    for mediaData in medias:
      results.append(streamfinder.Media.Media(self.database, mediaData))
    return results

  def getMediasNotStarredIn(self):
    results = []
    medias = self.database.query('SELECT * FROM Media WHERE media_id NOT IN (SELECT media_id FROM StarsIn WHERE actor_id = %s)', (self.actor_id, ))
    for mediaData in medias:
      results.append(streamfinder.Media.Media(self.database, mediaData))
    return results

  def setStarredMedias(self, mediaList):
    self.database.beginTransaction(streamfinder.database.IsolationLevel.READ_COMMITTED)
    cursor = self.database.conn.cursor()
    try:
      cursor.execute('DELETE FROM StarsIn WHERE actor_id = %s', (self.actor_id, ))
      for media in mediaList:
        cursor.execute('INSERT INTO StarsIn(media_id, actor_id) VALUES (%s, %s)', (media.getId(), self.actor_id))
      cursor.close()
      self.database.commitTransaction()
    except:
      cursor.close()
      self.database.rollbackTransaction()

  def addRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.execute('INSERT INTO ActorRating(actor_id, user_id, score) VALUES (%s, %s, %s)', (self.actor_id, userID, score))

  def updateRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.execute('UPDATE ActorRating SET score = %s WHERE actor_id = %s AND user_id = %s', (score, self.actor_id, userID))

  def deleteRating(self, userID):
    self.database.execute('DELETE FROM ActorRating WHERE actor_id = %s AND user_id = %s', (self.actor_id, userID))

  def getAverageRating(self):
    if 'averageRating' in self.data:
      return self.data['averageRating']
    result = self.database.query('SELECT AVG(score) AS rating FROM ActorRating WHERE actor_id = %s', (self.actor_id, ))
    self.data['averageRating'] = result[0]['rating']
    return self.data['averageRating']