import streamfinder.Media
import streamfinder.database

class Actor:

  def __init__(self, database, actor_id):
    self.database = database
    self.actor_id = actor_id

  def toDict(self):
    result = self.database.query('SELECT * FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    return dict(result[0])

  def getId(self):
    return self.actor_id

  def getName(self):
    result = self.database.query('SELECT name FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    return result[0]['name']

  def setName(self, name):
    self.database.execute('UPDATE Actor SET name = %s WHERE actor_id = %s', (name, self.actor_id))

  def getSex(self):
    result = self.database.query('SELECT sex FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    return result[0]['sex']

  def setSex(self, sex):
    self.database.execute('UPDATE Actor SET sex = %s WHERE actor_id = %s', (sex, self.actor_id))

  def getBirthDate(self):
    result = self.database.query('SELECT birthDate FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    return result[0]['birthDate']

  def setBirthDate(self, birthDate):
    self.database.execute('UPDATE Actor SET birthDate = %s WHERE actor_id = %s', (birthDate, self.actor_id))

  def getStarredMedias(self):
    medias = []
    results = self.database.query('SELECT media_id FROM StarsIn WHERE actor_id = %s', (self.actor_id, ))
    for media in results:
      medias.append(streamfinder.Media.Media(self.database, media['media_id']))
    return medias

  def getMediasNotStarredIn(self):
    medias = []
    results = self.database.query('SELECT media_id FROM Media WHERE media_id NOT IN (SELECT media_id FROM StarsIn WHERE actor_id = %s)', (self.actor_id, ))
    for media in results:
      medias.append(streamfinder.Media.Media(self.database, media['media_id']))
    return medias

  def setStarredMedias(self, mediaList):
    self.database.beginTransaction(streamfinder.database.IsolationLevel.SERIALIZABLE)
    cursor = self.database.conn.cursor()
    try:
      cursor.execute('DELETE FROM StarsIn WHERE actor_id = %s', (self.actor_id, ))
      for media in mediaList:
        cursor.execute('INSERT INTO StarsIn(media_id, actor_id) VALUES (%s, %s)', (media.getId(), self.actor_id))
      cursor.close()
      self.database.commitTransaction()
    except:
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
    result = self.database.query('SELECT AVG(score) AS rating FROM ActorRating WHERE actor_id = %s', (self.actor_id, ))
    return result[0]['rating']