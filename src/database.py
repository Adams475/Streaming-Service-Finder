import mysql.connector
from enum import Enum


# Enum for setting isolation levels
class IsolationLevel(Enum):
    READ_UNCOMMITTED = "READ UNCOMMITTED"
    READ_COMMITTED = "READ COMMITTED"
    REPEATABLE_READ = "REPEATABLE READ"
    SERIALIZABLE = "SERIALIZABLE"

from StreamingService import StreamingService
from Genre import Genre
from Director import Director
from Actor import Actor
from User import User
from Media import Media

class Database:

    ### Set up connection with MySQL database on Google Cloud
    def __init__(self):
        self.conn = None
        while self.conn is None:
            try:
                self.conn = mysql.connector.connect(
                    host="35.225.83.254",
                    user="root",
                    password="streamfinderCS348!",
                    database="streamfinder"
                )
            except:
                print("Failed to connect: trying again.")

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
    ### Uses READ UNCOMMITTED unless specified otherwise
    def query(self, query, arguments=(), isolationLevel=IsolationLevel.READ_UNCOMMITTED):

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
    ### Uses READ COMMITTED unless specified otherwise
    def execute(self, command, arguments=(), isolationLevel=IsolationLevel.READ_COMMITTED):
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
            print("Error in execute")
            print(f"Command: {command} with arguments {arguments}")
            self.rollbackTransaction()
            cursor.close()
            return None

    ###########################################################################

    def getStreamingService(self, ss_id):
        ssData = self.query('SELECT * FROM StreamingService WHERE ss_id = %s', (ss_id,))
        if len(ssData) == 0:
            return None
        return StreamingService(self, ssData[0])

    def getStreamingServiceByName(self, name):
        name = name.lower()
        services = self.query('SELECT * FROM StreamingService WHERE LOWER(name) LIKE %s', (name,))
        output = []
        for serviceData in services:
            output.append(StreamingService(self, serviceData))
        return output

    def getGenre(self, genre_id):
        genreData = self.query('SELECT * FROM Genre WHERE genre_id = %s', (genre_id,))
        if len(genreData) == 0:
            return None
        return Genre(self, genreData[0])

    def getGenreByName(self, name):
        name = name.lower()
        genres = self.query('SELECT * FROM Genre WHERE LOWER(name) LIKE %s', (name,))
        output = []
        for genreData in genres:
            output.append(Genre(self, genreData))
        return output

    def getDirector(self, director_id):
        directorData = self.query('SELECT * FROM Director WHERE director_id = %s', (director_id,))
        if len(directorData) == 0:
            return None
        return Director(self, directorData[0])

    def getDirectorByName(self, name):
        name = name.lower()
        directors = self.query('SELECT * FROM Director WHERE LOWER(name) LIKE %s', (name,))
        output = []
        for directorData in directors:
            output.append(Director(self, directorData))
        return output

    def getActor(self, actor_id):

        actorData = self.query('SELECT * FROM Actor WHERE actor_id = %s', (actor_id,))
        if len(actorData) == 0:
            return None
        return Actor(self, actorData[0])

    def getActorByName(self, name):
        name = name.lower()
        actors = self.query('SELECT * FROM Actor WHERE LOWER(name) LIKE %s', (name,))
        output = []
        for actorData in actors:
            output.append(Actor(self, actorData))
        return output

    def getUser(self, user_id):
        userData = self.query('SELECT * FROM User WHERE user_id = %s', (user_id,))
        if len(userData) == 0:
            return None
        return User(self, userData[0])

    def getUserByUsername(self, username):
        userData = self.query('SELECT * FROM User WHERE username LIKE %s', (username,))
        if len(userData) == 0:
            return None
        return User(self, userData[0])

    def getMedia(self, media_id):
        mediaData = self.query('SELECT * FROM Media WHERE media_id = %s', (media_id,))
        if (len(mediaData) == 0):
            return None
        return Media(self, mediaData[0])

    def getMediaByName(self, name):
        name = name.lower()
        medias = self.query('SELECT * FROM Media WHERE LOWER(name) LIKE %s', (name,))
        output = []
        for mediaData in medias:
            output.append(Media(self, mediaData))
        return output

    def getAllStreamingServices(self):
        streamingServices = self.query('SELECT * FROM StreamingService')
        result = []
        for serviceData in streamingServices:
            result.append(StreamingService(self, serviceData))
        return result

    def getAllGenres(self):
        genres = self.query('SELECT * FROM Genre')
        result = []
        for genreData in genres:
            result.append(Genre(self, genreData))
        return result

    def getAllDirectors(self):
        directors = self.query('SELECT * FROM Director')
        result = []
        for directorData in directors:
            result.append(Director(self, directorData))
        return result

    def getAllActors(self):
        actors = self.query('SELECT * FROM Actor')
        result = []
        for actorData in actors:
            result.append(Actor(self, actorData))
        return result

    def getAllUsers(self):
        users = self.query('SELECT * FROM User')
        result = []
        for userData in users:
            result.append(User(self, userData))
        return result

    def getAllMedias(self):
        medias = self.query('SELECT * FROM Media')
        result = []
        for mediaData in medias:
            result.append(Media(self, mediaData))
        return result

    def createUser(self, username, hashedPassword):
        user_id = self.execute('INSERT INTO User(username, hashedPassword) VALUES (%s, %s)', (username, hashedPassword))
        return User(self, {'user_id': user_id, 'username': username, 'hashedPassword': hashedPassword})

    def createGenre(self, name, description=''):
        genre_id = self.execute('INSERT INTO Genre(name, description) VALUES(%s, %s)', (name, description))
        return Genre(self, {'genre_id': genre_id, 'name': name, 'description': description})

    def createStreamingService(self, name):
        ss_id = self.execute('INSERT INTO StreamingService(name) VALUES(%s)', (name,))
        return StreamingService(self, {'ss_id': ss_id, 'name': name})

    def createActor(self, name, sex='Unspecified', birthDate='?'):
        actor_id = self.execute('INSERT INTO Actor(name, sex, birthDate) VALUES(%s, %s, %s)', (name, sex, birthDate))
        return Actor(self, {'actor_id': actor_id, 'name': name, 'sex': sex, 'birthDate': birthDate})

    def createDirector(self, name, sex='Unspecified', birthDate='?'):
        director_id = self.execute('INSERT INTO Director(name, sex, birthDate) VALUES(%s, %s, %s)',
                                   (name, sex, birthDate))
        return Director(self, {'director_id': director_id, 'name': name, 'sex': sex, 'birthDate': birthDate})

    def createMedia(self, name, year, genre, director):
        media_id = self.execute('INSERT INTO Media(name, releaseYear, genre_id, director_id) VALUES(%s, %s, %s, %s)',
                                (name, year, genre.getId(), director.getId()))
        return Media(self, {'media_id': media_id, 'name': name, 'releaseYear': year, 'genre_id': genre.getId(), 'director_id': director.getId()})

    ########### Specifc Queries for Webpages ###########

    ### Get table rows for all medias page (viewMedias.html)
    def getMediaTableRows(self):
        rows = self.query('SELECT M.name AS mediaName, M.media_id, M.releaseYear, '
                          '  G.name AS genreName, G.genre_id, D.name AS directorName, D.director_id, '
                          '  AVG(MediaRating.score) AS averageRating '
                          'FROM (Media M LEFT OUTER JOIN MediaRating ON M.media_id = MediaRating.media_id)'
                          '  JOIN Genre G ON M.genre_id = G.genre_id '
                          '  JOIN Director D ON M.director_id = D.director_id '
                          'GROUP BY M.media_id')
        return rows

    ### Get table rows for all actors page (viewActors.html)
    def getActorTableRows(self):
        rows = self.query('SELECT Actor.actor_id, name, sex, birthDate, AVG(score) AS averageRating '
                          'FROM Actor LEFT OUTER JOIN ActorRating ON Actor.actor_id = ActorRating.actor_id '
                          'GROUP BY actor_id')
        return rows

    ### Get table rows for all directors page (viewDirectors.html)
    def getDirectorTableRows(self):
        rows = self.query('SELECT Director.director_id, name, sex, birthDate, AVG(score) AS averageRating '
                          'FROM Director LEFT OUTER JOIN DirectorRating ON Director.director_id = DirectorRating.director_id '
                          'GROUP BY director_id')
        return rows

    ### Get table rows for recently added media on main page (index.html)
    def getRecentlyAddedMediaRows(self):
        rows = self.query('SELECT M.name AS mediaName, M.media_id, M.releaseYear, '
                          '  G.name AS genreName, G.genre_id, D.name AS directorName, D.director_id, '
                          '  AVG(MediaRating.score) AS averageRating '
                          'FROM (Media M LEFT OUTER JOIN MediaRating ON M.media_id = MediaRating.media_id)'
                          '  JOIN Genre G ON M.genre_id = G.genre_id '
                          '  JOIN Director D ON M.director_id = D.director_id '
                          'GROUP BY M.media_id '
                          'ORDER BY M.media_id DESC '
                          'LIMIT 5')
        return rows

    ### Get table rows for top-rated media on main page (index.html)
    def getHighestRatedMediaRows(self):
        rows = self.query('SELECT M.name AS mediaName, M.media_id, M.releaseYear, '
                          '  G.name AS genreName, G.genre_id, D.name AS directorName, D.director_id, '
                          '  AVG(MediaRating.score) AS averageRating '
                          'FROM (Media M NATURAL JOIN MediaRating)'
                          '  JOIN Genre G ON M.genre_id = G.genre_id '
                          '  JOIN Director D ON M.director_id = D.director_id '
                          'GROUP BY M.media_id '
                          'ORDER BY averageRating DESC '
                          'LIMIT 5')
        return rows

    ### Gets the number of each entity for the site statistics on the main page (index.html)
    def getEntityCounts(self):
        rows = self.query('SELECT "Users" AS type, COUNT(*) AS count FROM User '
                          'UNION SELECT "Movies/Shows" AS type, COUNT(*) AS count FROM Media '
                          'UNION SELECT "Actors" AS type, COUNT(*) AS count FROM Actor '
                          'UNION SELECT "Directors" AS type, COUNT(*) AS count FROM Director '
                          'UNION SELECT "Genres" AS type, COUNT(*) AS count FROM Genre '
                          'UNION SELECT "Streaming Services" AS type, COUNT(*) AS count FROM StreamingService')
        return rows

    ### Gets the number of medias per genre
    def getGenreStats(self):
        result = self.query('SELECT COUNT(media_id), g.name '
                            'FROM Media as m JOIN Genre as g on m.genre_id = g.genre_id '
                            'GROUP BY m.genre_id')
        return result
