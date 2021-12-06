import json

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
    self.database.conn.execute(f'UPDATE Actor SET name = "{name}" WHERE actor_id = {self.actor_id}')
    self.database.conn.commit()

  def getSex(self):
    result = self.database.query('SELECT sex FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    return result[0]['sex']

  def setSex(self, sex):
    self.database.conn.execute(f'UPDATE Actor SET sex = "{sex}" WHERE actor_id = {self.actor_id}')
    self.database.conn.commit()

  def getBirthDate(self):
    result = self.database.query('SELECT birthDate FROM Actor WHERE actor_id = %s', (self.actor_id, ))
    return result[0]['birthDate']

  def setName(self, birthDate):
    self.database.conn.execute(f'UPDATE Actor SET birthDate = "{birthDate}" WHERE actor_id = {self.actor_id}')
    self.database.conn.commit()

  def addRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.conn.execute(f'INSERT INTO ActorRating(actor_id, user_id, score) VALUES ({self.getId()}, {userID}, {score})')
    self.database.conn.commit()

  def updateRating(self, userID, score):
    if score < 0:
      score = 0
    elif score > 100:
      score = 100
    self.database.conn.execute(f'UPDATE ActorRating SET score = {score} WHERE actor_id = {self.getId()} AND user_id = {userID}')
    self.database.conn.commit()

  def deleteRating(self, userID):
    self.database.conn.execute(f'DELETE FROM ActorRating WHERE actor_id = {self.getId()} AND user_id = {userID}')
    self.database.conn.commit()

