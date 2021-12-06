class Director:

  def __init__(self, database, director_id):
    self.database = database
    self.director_id = director_id

  def toDict(self):
    result = self.database.query('SELECT * FROM Director WHERE director_id = %s', (self.director_id, ))
    return dict(result[0])

  def getId(self):
    return self.director_id

  def getName(self):
    result = self.database.query('SELECT name FROM Director WHERE director_id = %s', (self.director_id, ))
    return result[0]['name']

  def setName(self, name):
    self.database.execute('UPDATE Director SET name = %s WHERE director_id = %s', (name, self.director_id))

  def getSex(self):
    result = self.database.query('SELECT sex FROM Director WHERE director_id = %s', (self.director_id, ))
    return result[0]['sex']

  def setSex(self, sex):
    self.database.execute('UPDATE Director SET sex = %s WHERE director_id = %s', (sex, self.director_id))

  def getBirthDate(self):
    result = self.database.query('SELECT birthDate FROM Director WHERE director_id = %s', (self.director_id, ))
    return result[0]['birthDate']

  def setBirthDate(self, birthDate):
    self.database.execute('UPDATE Director SET birthDate = %s WHERE director_id = %s', (birthDate, self.director_id))

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