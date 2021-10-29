import json

class Director:

  def __init__(self, database, director_id):
    self.database = database
    self.director_id = director_id

  def serialize(self):
    result = self.database.conn.execute(f'SELECT * FROM Director WHERE director_id = {self.director_id}').fetchone()
    if result is None:
      return {}
    return json.dumps(dict(result))

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