import mysql.connector

from streamfinder.StreamingService import StreamingService
from streamfinder.Genre import Genre
from streamfinder.Director import Director
from streamfinder.Actor import Actor
from streamfinder.User import User
from streamfinder.Media import Media

class Database:

    ### Set up connection with MySQL database on Google Cloud
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="34.69.18.126",
            user="root",
            password="streamfinderCS348!",
            database="streamfinder"
        )

    ### Wrapper function for select statements, returns list of dicts of matches
    def query(self, query, arguments=(), printQueries=True):
        if printQueries:
            if len(arguments) > 0:
                print(f'\nHandled query: "{query}" - {arguments}')
            else:
                print(f'\nHandled query: "{query}"')
        cursor = self.conn.cursor()
        cursor.execute(query, arguments)
        columns = cursor.description
        result = []
        for value in cursor.fetchall():
            tmp = {}
            for (index, column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)
        if printQueries:
            print(result)
        return result

    def getStreamingService(self, ss_id):
        result = self.query('SELECT COUNT(*) AS cnt FROM StreamingService WHERE ss_id = %s', (ss_id, ))
        if result[0]['cnt'] == 0:
            return None
        return StreamingService(self, ss_id)

    def getStreamingServiceByName(self, name):
        name = name.lower()
        services = self.query('SELECT ss_id FROM StreamingService WHERE LOWER(name) LIKE "%s"', (name, ))
        output = []
        for service in services:
            output.append(StreamingService(self, service['ss_id']))
        return output

    def getGenre(self, genre_id):
        result = self.query('SELECT COUNT(*) AS cnt FROM Genre WHERE genre_id = %s', (genre_id, ))
        if result[0]['cnt'] == 0:
            return None
        return Genre(self, genre_id)

    def getGenreByName(self, name):
        name = name.lower()
        genres = self.query('SELECT genre_id FROM Genre WHERE LOWER(name) LIKE "%s"', (name, ))
        output = []
        for genre in genres:
            output.append(Genre(self, genre['genre_id']))
        return output

    def getDirector(self, director_id):
        result = self.query('SELECT COUNT(*) AS cnt FROM Director WHERE director_id = %s', (director_id))
        if result[0]['cnt'] == 0:
            return None
        return Director(self, director_id)

    def getDirectorByName(self, name):
        name = name.lower()
        directors = self.query('SELECT director_id FROM Director WHERE LOWER(name) LIKE "%s"', (name, ))
        output = []
        for director in directors:
            output.append(Director(self, director['director_id']))
        return output

    def getActor(self, actor_id):
        result = self.query('SELECT COUNT(*) AS cnt FROM Actor WHERE actor_id = %s', (actor_id, ))
        if result[0]['cnt'] == 0:
            return None
        return Actor(self, actor_id)

    def getActorByName(self, name):
        name = name.lower()
        actors = self.query('SELECT actor_id FROM Actor WHERE LOWER(name) LIKE "%s"', (name, ))
        output = []
        for actor in actors:
            output.append(Actor(self, actor['actor_id']))
        return output

    def getUser(self, user_id):
        result = self.query('SELECT COUNT(*) AS cnt FROM User WHERE user_id = %s', (user_id, ))
        if result[0]['cnt'] == 0:
            return None
        return User(self, user_id)

    def getUserByUsername(self, username):
        result = self.query('SELECT user_id FROM User WHERE username = "%s"', (username, ))
        if len(result) == 0:
            return None
        return User(self, result['user_id'])

    def getMedia(self, media_id):
        result = self.query('SELECT COUNT(*) AS cnt FROM Media WHERE media_id = %s', (media_id, ))
        if result[0]['cnt'] == 0:
            return None
        return Media(self, media_id)

    def getMediaByName(self, name):
        name = name.lower()
        medias = self.query('SELECT media_id FROM Media WHERE LOWER(name) LIKE "%s"', (name, ))
        output = []
        for media in medias:
            output.append(Media(self, media['media_id']))
        return output

    def getAllStreamingServices(self):
        streamingServices = self.query('SELECT ss_id FROM StreamingService')
        result = []
        for service in streamingServices:
            result.append(StreamingService(self, service['ss_id']))
        return result

    def getAllGenres(self):
        genres = self.query('SELECT genre_id FROM Genre')
        result = []
        for genre in genres:
            result.append(Genre(self, genre['genre_id']))
        return result

    def getAllDirectors(self):
        directors = self.query('SELECT director_id FROM Director')
        result = []
        for director in directors:
            result.append(Director(self, director['director_id']))
        return result

    def getAllActors(self):
        actors = self.query('SELECT actor_id FROM Actor')
        result = []
        for actor in actors:
            result.append(Actor(self, actor['actor_id']))
        return result

    def getAllUsers(self):
        users = self.query('SELECT user_id FROM User')
        result = []
        for user in users:
            result.append(User(self, user['user_id']))
        return result

    def getAllMedias(self):
        medias = self.query('SELECT media_id FROM Media')
        result = []
        for media in medias:
            result.append(Media(self, media['media_id']))
        return result

    def createUser(self, username, hashedPassword):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO User(username, hashedPassword) VALUES (?, ?)', (username, hashedPassword))
        user_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return User(self, user_id)

    def createGenre(self, name, description=''):
        cursor = self.conn.cursor()
        cursor.execute(f'INSERT INTO Genre(name, description) VALUES("{name}", "{description}")')
        genre_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return Genre(self, genre_id)

    def createStreamingService(self, name):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO StreamingService(name) VALUES(%s)', (name,))
        ss_id = cursor.lastrowid
        self.conn.commit()
        return StreamingService(self, ss_id)

    def createActor(self, name, sex='Unspecified', birthDate='?'):
        cursor = self.conn.cursor()
        cursor.execute(f'INSERT INTO Actor(name, sex, birthDate) VALUES("{name}", "{sex}", "{birthDate}")')
        actor_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return Actor(self, actor_id)

    def createDirector(self, name, sex='Unspecified', birthDate='?'):
        cursor = self.conn.cursor()
        cursor.execute(f'INSERT INTO Director(name, sex, birthDate) VALUES("{name}", "{sex}", "{birthDate}")')
        director_id = cursor.lastrowid
        cursor.close()
        self.conn.commit()
        return Director(self, director_id)

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
        return Media(self, media_id)

