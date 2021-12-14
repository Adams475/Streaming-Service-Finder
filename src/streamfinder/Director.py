import streamfinder.Media

class Director:

  def __init__(self, database, directorData):
    self.database = database
    self.director_id = directorData['director_id']
    self.data = directorData

  def toDict(self):
    result = self.database.query('SELECT * FROM Director WHERE director_id = %s', (self.director_id, ))
    return dict(result[0])

  def getId(self):
    return self.director_id

  def getName(self):
    if 'name' in self.data:
      return self.data['name']
    result = self.database.query('SELECT name FROM Director WHERE director_id = %s', (self.director_id, ))
    self.data['name'] = result[0]['name']
    return self.data['name']

  def setName(self, name):
    self.database.execute('UPDATE Director SET name = %s WHERE director_id = %s', (name, self.director_id))

  def getSex(self):
    if 'sex' in self.data:
      return self.data['sex']
    result = self.database.query('SELECT sex FROM Director WHERE director_id = %s', (self.director_id, ))
    self.data['sex'] = result[0]['sex']
    return self.data['sex']

  def setSex(self, sex):
    self.database.execute('UPDATE Director SET sex = %s WHERE director_id = %s', (sex, self.director_id))

  def getBirthDate(self):
    if 'birthDate' in self.data:
      return self.data['birthDate']
    result = self.database.query('SELECT birthDate FROM Director WHERE director_id = %s', (self.director_id, ))
    self.data['birthDate'] = result[0]['birthDate']
    return self.data['birthDate']

  def setBirthDate(self, birthDate):
    self.database.execute('UPDATE Director SET birthDate = %s WHERE director_id = %s', (birthDate, self.director_id))

  def getDirectedMedias(self):
    results = []
    medias = self.database.query('SELECT * FROM Media WHERE director_id = %s', (self.director_id, ))
    for mediaData in medias:
      results.append(streamfinder.Media.Media(self.database, mediaData))
    return results

  def addRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.execute('INSERT INTO DirectorRating(director_id, user_id, score) VALUES (%s, %s, %s)', (self.director_id, userID, score))

  def updateRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.execute('UPDATE DirectorRating SET score = %s WHERE director_id = %s AND user_id = %s', (score, self.director_id, userID))

  def deleteRating(self, userID):
    self.database.execute('DELETE FROM DirectorRating WHERE director_id = %s AND user_id = %s', (self.director_id, userID))

  def getAverageRating(self):
    if 'averageRating' in self.data:
      return self.data['averageRating']
    result = self.database.query('SELECT AVG(score) AS rating FROM DirectorRating WHERE director_id = %s', (self.director_id, ))
    self.data['averageRating'] = result[0]['rating']
    return self.data['averageRating']