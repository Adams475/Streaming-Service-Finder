import streamfinder.Media

class Genre:

  def __init__(self, database, genreData):
    self.database = database
    self.genre_id = genreData['genre_id']
    self.data = genreData

  def toDict(self):
    result = self.database.query('SELECT * FROM Genre WHERE genre_id = %s', (self.genre_id, ))
    return dict(result[0])

  def getId(self):
    return self.genre_id

  def getName(self):
    if 'name' in self.data:
      return self.data['name']
    result = self.database.query('SELECT name FROM Genre WHERE genre_id = %s', (self.genre_id, ))
    self.data['name'] = result[0]['name']
    return self.data['name']

  def setName(self, name):
    self.database.execute('UPDATE Genre SET name = %s WHERE genre_id = %s', (name, self.genre_id))

  def getDescription(self):
    if 'description' in self.data:
      return self.data['description']
    result = self.database.query('SELECT description FROM Genre WHERE genre_id = %s', (self.genre_id, ))
    self.data['description'] = result[0]['description']
    return self.data['description']

  def setDescription(self, description):
    self.database.execute('UPDATE Genre SET description = %s WHERE genre_id = %s', (description, self.genre_id))

  def getCorrespondingMedia(self):
    results = []
    medias = self.database.query('SELECT * FROM Media WHERE genre_id = %s', (self.genre_id, ))
    for mediaData in medias:
      results.append(streamfinder.Media.Media(self.database, mediaData))
    return results