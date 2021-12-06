import json

from streamfinder.Actor import Actor
from streamfinder.Director import Director
from streamfinder.Media import Media

class User:

  def __init__(self, database, user_id):
    self.database = database
    self.user_id = user_id

  def toDict(self):
    result = self.database.query('SELECT user_id, username FROM User WHERE user_id = %s', (self.user_id, ))
    return dict(result[0])

  def getId(self):
    return self.user_id

  def getUsername(self):
    result = self.database.query('SELECT username FROM User WHERE user_id = %s', (self.user_id, ))
    return result[0]['username']

  def setUsername(self, username):
    self.database.conn.execute(f'UPDATE User SET username = {username} WHERE user_id = {self.user_id}')
    self.database.conn.commit()

  def getHashedPassword(self):
    result = self.database.query('SELECT hashedPassword FROM User WHERE user_id = %s', (self.user_id, ))
    return result[0]['hashedPassword']

  def setHashedPassword(self, hashedPassword):
    self.database.conn.execute(f'UPDATE User SET hashedPassword = {hashedPassword} WHERE user_id = {self.user_id}')
    self.database.conn.commit()

  def getRatings(self):
    ratings = {}

    ### Actors ###
    actorRatings = self.database.query('SELECT actor_id, name, score FROM ActorRating NATURAL JOIN Actor WHERE user_id = %s', (self.user_id, ))
    ratings['actorRatings'] = actorRatings

    ### Media ###
    mediaRatings = self.database.query('SELECT media_id, name, score FROM MediaRating NATURAL JOIN Media WHERE user_id = %s', (self.user_id, ))
    ratings['mediaRatings'] = mediaRatings

    ### Directors ###
    directorRatings = self.database.query('SELECT director_id, name, score FROM DirectorRating NATURAL JOIN Director WHERE user_id = %s', (self.user_id, ))
    ratings['directorRatings'] = directorRatings

    return ratings

  def getActorsNotRated(self):
    actors = []
    results = self.database.query('SELECT actor_id FROM Actor WHERE actor_id NOT IN (SELECT actor_id FROM ActorRating WHERE user_id = %s)', (self.user_id, ))
    for actor in results:
      actors.append(Actor(self.database, actor['actor_id']))
    return actors

  def getDirectorsNotRated(self):
    directors = []
    results = self.database.query('SELECT director_id FROM Director WHERE director_id NOT IN (SELECT director_id FROM DirectorRating WHERE user_id = %s)', (self.user_id, ))
    for director in results:
      directors.append(Director(self.database, director['director_id']))
    return directors

  def getMediasNotRated(self):
    medias = []
    results = self.database.query('SELECT media_id FROM Media WHERE media_id NOT IN (SELECT media_id FROM MediaRating WHERE user_id = %s)', (self.user_id, ))
    for media in results:
      medias.append(Media(self.database, media['media_id']))
    return medias