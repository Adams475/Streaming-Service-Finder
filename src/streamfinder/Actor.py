import json

class Actor:

  def __init__(self, database, actor_id):
    self.database = database
    self.actor_id = actor_id

  def serialize(self):
    result = self.database.conn.execute(f'SELECT * FROM Actor WHERE actor_id = {self.actor_id}').fetchone()
    if result is None:
      return {}
    return json.dumps(dict(result))

  def getId(self):
    return self.actor_id

  def getName(self):
    result = self.database.conn.execute(f'SELECT name FROM Actor WHERE actor_id = {self.actor_id}').fetchone()
    return result['name']

  def setName(self, name):
    self.database.conn.execute(f'UPDATE Actor SET name = {name} WHERE actor_id = {self.actor_id}')
    self.database.conn.commit()

  def getSex(self):
    result = self.database.conn.execute(f'SELECT sex FROM Actor WHERE actor_id = {self.actor_id}').fetchone()
    return result['sex']

  def setSex(self, sex):
    self.database.conn.execute(f'UPDATE Actor SET sex = {sex} WHERE actor_id = {self.actor_id}')
    self.database.conn.commit()

  def getBirthDate(self):
    result = self.database.conn.execute(f'SELECT birthDate FROM Actor WHERE actor_id = {self.actor_id}').fetchone()
    return result['birthDate']

  def setName(self, birthDate):
    self.database.conn.execute(f'UPDATE Actor SET birthDate = {birthDate} WHERE actor_id = {self.actor_id}')
    self.database.conn.commit()
