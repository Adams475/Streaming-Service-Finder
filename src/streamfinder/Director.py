import json

class Director:

  def __init__(self, database, director_id):
    self.database = database
    self.director_id = director_id

  def toDict(self):
    result = self.database.conn.execute(f'SELECT * FROM Director WHERE director_id = {self.director_id}').fetchone()
    if result is None:
      return {}
    return dict(result)

  def getId(self):
    return self.director_id

  def getName(self):
    result = self.database.conn.execute(f'SELECT name FROM Director WHERE director_id = {self.director_id}').fetchone()
    return result['name']

  def setName(self, name):
    self.database.conn.execute(f'UPDATE Director SET name = {name} WHERE director_id = {self.director_id}')
    self.database.conn.commit()

  def getSex(self):
    result = self.database.conn.execute(f'SELECT sex FROM Director WHERE director_id = {self.director_id}').fetchone()
    return result['sex']

  def setSex(self, sex):
    self.database.conn.execute(f'UPDATE Director SET sex = {sex} WHERE director_id = {self.director_id}')
    self.database.conn.commit()

  def getBirthDate(self):
    result = self.database.conn.execute(f'SELECT birthDate FROM Director WHERE director_id = {self.director_id}').fetchone()
    return result['birthDate']

  def setName(self, birthDate):
    self.database.conn.execute(f'UPDATE Director SET birthDate = {birthDate} WHERE director_id = {self.director_id}')
    self.database.conn.commit()

  def addRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.conn.execute(f'INSERT INTO DirectorRating(director_id, user_id, score) VALUES ({self.getId()}, {userID}, {score})')
    self.database.conn.commit()

  def updateRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.conn.execute(f'UPDATE DirectorRating SET score = {score} WHERE director_id = {self.getId()} AND user_id = {userID})')
    self.database.conn.commit()

  def deleteRating(self, userID):
    self.database.conn.execute(f'DELETE FROM DirectorRating WHERE director_id = {self.getId()} AND user_id = {userID}')
    self.database.conn.commit()