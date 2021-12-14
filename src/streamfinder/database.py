import mysql.connector
from enum import Enum

# Enum for setting isolation levels
class IsolationLevel(Enum):
    READ_UNCOMMITTED = "READ UNCOMMITTED"
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"

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

    ### Wrapper function that begins a transaction with the specified isolation level (from enum)
    def beginTransaction(self, isolationLevel):
        self.conn.start_transaction(isolation_level=isolationLevel.value)

    ### Wrapper function to commit a transaction
    def commitTransaction(self):
        self.conn.commit()

    ### Wrapper function to rollback a transaction
    def rollbackTransaction(self):
        self.conn.rollback()

    ### Wrapper function for select statements, returns list of dicts of matches
    ### Uses READ COMMITTED unless specified otherwise
    def query(self, query, arguments=(), isolationLevel=IsolationLevel.READ_COMMITTED):

        self.beginTransaction(isolationLevel)

        cursor = self.conn.cursor()
        cursor.execute(query, arguments)
        columns = cursor.description
        result = []
        for value in cursor.fetchall():
            tmp = {}
            for (index, column) in enumerate(value):
                tmp[columns[index][0]] = column
            result.append(tmp)

        cursor.close()
        self.commitTransaction()

        print(f"\nHandled Query: '{query}' with arguments '{arguments}'")
        print(result)
        return result

    ### Wrapper function to execute insert/update/delete statements using the specified isolation level
    ### Uses REPEATABLE READ unless specified otherwise
    def execute(self, command, arguments=(), isolationLevel=IsolationLevel.REPEATABLE_READ):
        print(f"\nHandled Command: '{command}' with arguments '{arguments}'")
        self.beginTransaction(isolationLevel)
        cursor = self.conn.cursor()
        try:
            cursor.execute(command, arguments)
            row = cursor.lastrowid
            self.commitTransaction()
            cursor.close()
            return row
        except:
            print("Error in runSQL")
            print(f"Command: {command} with arguments {arguments}")
            self.rollbackTransaction()
            cursor.close()
            return None

    ###########################################################################

    def getStreamingService(self, ss_id):
        result = self.query('SELECT COUNT(*) AS cnt FROM StreamingService WHERE ss_id = %s', (ss_id, ))
        if result[0]['cnt'] == 0:
            return None
        return StreamingService(self, ss_id)

    def getStreamingServiceByName(self, name):
        name = name.lower()
        services = self.query('SELECT ss_id FROM StreamingService WHERE LOWER(name) LIKE %s', (name, ))
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
        genres = self.query('SELECT genre_id FROM Genre WHERE LOWER(name) LIKE %s', (name, ))
        output = []
        for genre in genres:
            output.append(Genre(self, genre['genre_id']))
        return output

    def getDirector(self, director_id):
        result = self.query('SELECT COUNT(*) AS cnt FROM Director WHERE director_id = %s', (director_id, ))
        if result[0]['cnt'] == 0:
            return None
        return Director(self, director_id)

    def getDirectorByName(self, name):
        name = name.lower()
        directors = self.query('SELECT director_id FROM Director WHERE LOWER(name) LIKE %s', (name, ))
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
        actors = self.query('SELECT actor_id FROM Actor WHERE LOWER(name) LIKE %s', (name, ))
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
        result = self.query('SELECT user_id FROM User WHERE username = %s', (username, ))
        if len(result) == 0:
            return None
        return User(self, result[0]['user_id'])

    def getMedia(self, media_id):
        result = self.query('SELECT COUNT(*) AS cnt FROM Media WHERE media_id = %s', (media_id, ))
        if result[0]['cnt'] == 0:
            return None
        return Media(self, media_id)

    def getMediaByName(self, name):
        name = name.lower()
        medias = self.query('SELECT media_id FROM Media WHERE LOWER(name) LIKE %s', (name, ))
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
        user_id = self.execute('INSERT INTO User(username, hashedPassword) VALUES (%s, %s)', (username, hashedPassword))
        return User(self, user_id)

    def createGenre(self, name, description=''):
        genre_id = self.execute('INSERT INTO Genre(name, description) VALUES(%s, %s)', (name, description))
        return Genre(self, genre_id)

    def createStreamingService(self, name):
        ss_id = self.execute('INSERT INTO StreamingService(name) VALUES(%s)', (name, ))
        return StreamingService(self, ss_id)

    def createActor(self, name, sex='Unspecified', birthDate='?'):
        actor_id = self.execute('INSERT INTO Actor(name, sex, birthDate) VALUES(%s, %s, %s)', (name, sex, birthDate))
        return Actor(self, actor_id)

    def createDirector(self, name, sex='Unspecified', birthDate='?'):
        director_id = self.execute('INSERT INTO Director(name, sex, birthDate) VALUES(%s, %s, %s)', (name, sex, birthDate))
        return Director(self, director_id)

    def createMedia(self, name, year, genre, director):
        media_id = self.execute('INSERT INTO Media(name, releaseYear, genre_id, director_id) VALUES(%s, %s, %s, %s)', (name, year, genre.getId(), director.getId()))
        return Media(self, media_id)

  
