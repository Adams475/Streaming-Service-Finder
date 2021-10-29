import json

class User:

  def __init__(self, database, user_id):
    self.database = database
    self.user_id = user_id

  def serialize(self):
    result = self.database.conn.execute(f'SELECT * FROM User WHERE user_id = {self.user_id}').fetchone()
    if result is None:
      return {}
    return json.dumps(dict(result))

  def getId(self):
    return self.user_id

  def getUsername(self):
    result = self.database.conn.execute(f'SELECT username FROM User WHERE user_id = {self.user_id}').fetchone()
    return result['username']

  def setUsername(self, username):
    self.database.conn.execute(f'UPDATE User SET username = {username} WHERE user_id = {self.user_id}')
    self.database.conn.commit()

  def getHashedPassword(self):
    result = self.database.conn.execute(f'SELECT hashedPassword FROM User WHERE user_id = {self.user_id}').fetchone()
    return result['hashedPassword']

  def setHashedPassword(self, hashedPassword):
    self.database.conn.execute(f'UPDATE User SET hashedPassword = {hashedPassword} WHERE user_id = {self.user_id}')
    self.database.conn.commit()