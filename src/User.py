import json

import Actor
import Director
import Media

class User:

  def __init__(self, database, userData):
    self.database = database
    self.user_id = userData['user_id']
    self.data = userData

  def toDict(self):
    result = self.database.query('SELECT user_id, username FROM User WHERE user_id = %s', (self.user_id, ))
    return dict(result[0])

  def getId(self):
    return self.user_id

  def getUsername(self):
    if 'username' in self.data:
      return self.data['username']
    result = self.database.query('SELECT username FROM User WHERE user_id = %s', (self.user_id, ))
    self.data['username'] = result[0]['username']
    return self.data['username']

  def setUsername(self, username):
    self.database.execute('UPDATE User SET username = %s WHERE user_id = %s', (username, self.user_id))

  def getHashedPassword(self):
    if 'hashedPassword' in self.data:
      return self.data['hashedPassword']
    result = self.database.query('SELECT hashedPassword FROM User WHERE user_id = %s', (self.user_id, ))
    self.data['hashedPassword'] = result[0]['hashedPassword']
    return self.data['hashedPassword']

  def setHashedPassword(self, hashedPassword):
    self.database.execute('UPDATE User SET hashedPassword = %s WHERE user_id = %s', (hashedPassword, self.user_id))

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
    results = []
    actors = self.database.query('SELECT * FROM Actor WHERE actor_id NOT IN (SELECT actor_id FROM ActorRating WHERE user_id = %s)', (self.user_id, ))
    for actorData in actors:
      results.append(Actor.Actor(self.database, actorData))
    return results

  def getDirectorsNotRated(self):
    results = []
    directors = self.database.query('SELECT * FROM Director WHERE director_id NOT IN (SELECT director_id FROM DirectorRating WHERE user_id = %s)', (self.user_id, ))
    for directorData in directors:
      results.append(Director.Director(self.database, directorData))
    return results

  def getMediasNotRated(self):
    results = []
    medias = self.database.query('SELECT * FROM Media WHERE media_id NOT IN (SELECT media_id FROM MediaRating WHERE user_id = %s)', (self.user_id, ))
    for mediaData in medias:
      results.append(Media.Media(self.database, mediaData))
    return results