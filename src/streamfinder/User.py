import json

class User:

  def __init__(self, database, user_id):
    self.database = database
    self.user_id = user_id

  def toDict(self):
    result = self.database.conn.execute(f'SELECT user_id, username FROM User WHERE user_id = {self.user_id}').fetchone()
    if result is None:
      return {}
    return dict(result)

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

  def getRatings(self):
    ratings = {}

    ### Actors ###
    actorRatings = []
    results = self.database.conn.execute(f'SELECT actor_id, name, score FROM ActorRating NATURAL JOIN Actor WHERE user_id = {self.getId()}').fetchall()
    for result in results:
      actorRatings.append(dict(result))
    ratings['actorRatings'] = actorRatings

    ### Media ###
    mediaRatings = []
    results = self.database.conn.execute(f'SELECT media_id, name, score FROM MediaRating NATURAL JOIN Media WHERE user_id = {self.getId()}').fetchall()
    for result in results:
      mediaRatings.append(dict(result))
    ratings['mediaRatings'] = mediaRatings

    ### Directors ###
    directorRatings = []
    results = self.database.conn.execute(f'SELECT director_id, name, score FROM DirectorRating NATURAL JOIN Director WHERE user_id = {self.getId()}').fetchall()
    for result in results:
      directorRatings.append(dict(result))
    ratings['directorRatings'] = directorRatings

    return ratings

  def getActorsNotRated(self):
    actors = []
    results = self.database.conn.execute(f'SELECT actor_id FROM Actor WHERE actor_id NOT IN (SELECT actor_id FROM ActorRating WHERE user_id = {self.getId()})').fetchall()
    for actor in results:
      actors.append(self.database.getActor(actor['actor_id']))
    return actors

  def getDirectorsNotRated(self):
    directors = []
    results = self.database.conn.execute(f'SELECT director_id FROM Director WHERE director_id NOT IN (SELECT director_id FROM DirectorRating WHERE user_id = {self.getId()})').fetchall()
    for director in results:
      directors.append(self.database.getDirector(director['director_id']))
    return directors

  def getMediasNotRated(self):
    medias = []
    results = self.database.conn.execute(f'SELECT media_id FROM Media WHERE media_id NOT IN (SELECT media_id FROM MediaRating WHERE user_id = {self.getId()})').fetchall()
    for media in results:
      medias.append(self.database.getMedia(media['media_id']))
    return medias