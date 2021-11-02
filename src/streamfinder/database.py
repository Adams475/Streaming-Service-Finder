import sqlite3

from streamfinder.StreamingService import StreamingService
from streamfinder.Genre import Genre
from streamfinder.Director import Director
from streamfinder.Actor import Actor
from streamfinder.User import User
from streamfinder.Media import Media

class Database:

    def __init__(self):
        self.conn = sqlite3.connect('streamfinder.sqlite3')
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.conn.commit()

    def getStreamingService(self, ss_id):
        result = self.conn.execute(f'SELECT COUNT(*) FROM StreamingService WHERE ss_id = {ss_id}').fetchone()
        if result[0] == 0:
            return None
        return StreamingService(self, ss_id)

    def getStreamingServiceByName(self, name):
        name = name.lower()
        services = self.conn.execute(f'SELECT ss_id FROM StreamingService WHERE LOWER(name) LIKE "{name}"').fetchall()
        output = []
        for service in services:
            output.append(self.getStreamingService(service['ss_id']))
        return output

    def getGenre(self, genre_id):
        result = self.conn.execute(f'SELECT COUNT(*) FROM Genre WHERE genre_id = {genre_id}').fetchone()
        if result[0] == 0:
            return None
        return Genre(self, genre_id)

    def getGenreByName(self, name):
        name = name.lower()
        genres = self.conn.execute(f'SELECT genre_id FROM Genre WHERE LOWER(name) LIKE "{name}"').fetchall()
        output = []
        for genre in genres:
            output.append(self.getGenre(genre['genre_id']))
        return output

    def getDirector(self, director_id):
        result = self.conn.execute(f'SELECT COUNT(*) FROM Director WHERE director_id = {director_id}').fetchone()
        if result[0] == 0:
            return None
        return Director(self, director_id)

    def getDirectorByName(self, name):
        name = name.lower()
        directors = self.conn.execute(f'SELECT director_id FROM Director WHERE LOWER(name) LIKE "{name}"').fetchall()
        output = []
        for director in directors:
            output.append(self.getDirector(director['director_id']))
        return output

    def getActor(self, actor_id):
        result = self.conn.execute(f'SELECT COUNT(*) FROM Actor WHERE actor_id = {actor_id}').fetchone()
        if result[0] == 0:
            return None
        return Actor(self, actor_id)

    def getActorByName(self, name):
        name = name.lower()
        actors = self.conn.execute(f'SELECT actor_id FROM Actor WHERE LOWER(name) LIKE "{name}"').fetchall()
        output = []
        for actor in actors:
            output.append(self.getActor(actor['actor_id']))
        return output

    def getUser(self, user_id):
        result = self.conn.execute(f'SELECT COUNT(*) FROM User WHERE user_id = {user_id}').fetchone()
        if result[0] == 0:
            return None
        return User(self, user_id)

    def createUser(self, username, hashedPassword):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO User(username, hashedPassword) VALUES (?, ?)', (username, hashedPassword))
        user_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return self.getUser(user_id)

    def getMedia(self, media_id):
        result = self.conn.execute(f'SELECT COUNT(*) FROM Media WHERE media_id = {media_id}').fetchone()
        if result[0] == 0:
            return None
        return Media(self, media_id)

    def getAllStreamingServices(self):
        streamingServices = self.conn.execute('SELECT * FROM StreamingService')
        result = []
        for service in streamingServices:
            result.append(self.getStreamingService(service['ss_id']))
        return result

    def getAllGenres(self):
        genres = self.conn.execute('SELECT * FROM Genre')
        result = []
        for genre in genres:
            result.append(self.getGenre(genre['genre_id']))
        return result

    def getAllDirectors(self):
        directors = self.conn.execute('SELECT * FROM Director')
        result = []
        for director in directors:
            result.append(self.getDirector(director['director_id']))
        return result

    def getAllActors(self):
        actors = self.conn.execute('SELECT * FROM Actor')
        result = []
        for actor in actors:
            result.append(self.getActor(actor['actor_id']))
        return result

    def getAllUsers(self):
        users = self.conn.execute('SELECT * FROM User')
        result = []
        for user in users:
            result.append(self.getUser(user['user_id']))
        return result

    def getAllMedias(self):
        medias = self.conn.execute('SELECT * FROM Media')
        result = []
        for media in medias:
            result.append(self.getMedia(media['media_id']))
        return result

    def searchUserByUsername(self, username):
        result = self.conn.execute(f'SELECT user_id FROM User WHERE username = "{username}"').fetchone()
        if result is None:
            return None
        return User(self, result['user_id'])

    def createGenre(self, name, description=''):
        cursor = self.conn.cursor()
        cursor.execute(f'INSERT INTO Genre(name, description) VALUES("{name}", "{description}")')
        genre_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return self.getGenre(genre_id)

    def createStreamingService(self, name):
        cursor = self.conn.cursor()
        cursor.execute(f'INSERT INTO StreamingService(name) VALUES("{name}")')
        ss_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return self.getStreamingService(ss_id)

    def createActor(self, name, sex='Unspecified', birthDate='?'):
        cursor = self.conn.cursor()
        cursor.execute(f'INSERT INTO Actor(name, sex, birthDate) VALUES("{name}", "{sex}", "{birthDate}")')
        actor_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return self.getActor(actor_id)

    def createDirector(self, name, sex='Unspecified', birthDate='?'):
        cursor = self.conn.cursor()
        cursor.execute(f'INSERT INTO Director(name, sex, birthDate) VALUES("{name}", "{sex}", "{birthDate}")')
        director_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return self.getDirector(director_id)

    def createMedia(self, name, year, genre, director):
        cursor = self.conn.cursor()
        genre_id = self.getGenreByName(genre)[0].getId()
        director_id = self.getDirectorByName(director)[0].getId()
        print("Director id for " + director + " is " + str(director_id))
        cursor.execute(
            f'INSERT INTO Media(name, releaseYear, genre_id, director_id) VALUES("{name}", "{year}", "{genre_id}", "{director_id}")')
        media_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return self.getMedia(media_id)

    def getMediaByName(self, name):
        name = name.lower()
        medias = self.conn.execute(f'SELECT media_id FROM Media WHERE LOWER(name) LIKE "{name}"').fetchall()
        output = []
        for media in medias:
            output.append(self.getMedia(media['media_id']))
        return output

