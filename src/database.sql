DROP TABLE IF EXISTS StreamingService;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Director;
DROP TABLE IF EXISTS Actor;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Media;
DROP TABLE IF EXISTS ViewableOn;
DROP TABLE IF EXISTS StarsIn;
DROP TABLE IF EXISTS MediaRating;
DROP TABLE IF EXISTS ActorRating;
DROP TABLE IF EXISTS DirectorRating;

CREATE TABLE IF NOT EXISTS StreamingService(
  ss_id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Genre(
  genre_id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  description TEXT DEFAULT '' NOT NULL
);

CREATE TABLE IF NOT EXISTS Director(
  director_id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  sex TEXT DEFAULT 'Unspecified' NOT NULL,
  birthDate TEXT DEFAULT '?' NOT NULL
);

CREATE TABLE IF NOT EXISTS Actor(
  actor_id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  sex TEXT DEFAULT 'Unspecified' NOT NULL,
  birthDate TEXT DEFAULT '?' NOT NULL
);

CREATE TABLE IF NOT EXISTS User(
  user_id INTEGER PRIMARY KEY NOT NULL,
  username TEXT NOT NULL,
  hashedPassword TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Media(
  media_id INTEGER PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  releaseYear INTEGER DEFAULT -1 NOT NULL,
  genre_id INTEGER NOT NULL,
  director_id INTEGER NOT NULL,
  FOREIGN KEY(genre_id) REFERENCES Genre(genre_id),
  FOREIGN KEY(director_id) REFERENCES Director(director_id)
);

CREATE TABLE IF NOT EXISTS ViewableOn(
  media_id INTEGER NOT NULL,
  ss_id INTEGER NOT NULL,
  PRIMARY KEY(media_id, ss_id),
  FOREIGN KEY(media_id) REFERENCES Media(media_id) ON DELETE CASCADE,
  FOREIGN KEY(ss_id) REFERENCES StreamingService(ss_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS StarsIn(
  actor_id INTEGER NOT NULL,
  media_id INTEGER NOT NULL,
  PRIMARY KEY(actor_id, media_id),
  FOREIGN KEY(actor_id) REFERENCES Actor(actor_id) ON DELETE CASCADE,
  FOREIGN KEY(media_id) REFERENCES Media(media_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS MediaRating(
  media_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  score INTEGER NOT NULL,
  PRIMARY KEY(media_id, user_id),
  FOREIGN KEY(media_id) REFERENCES Media(media_id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ActorRating(
  actor_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  score INTEGER NOT NULL,
  PRIMARY KEY(actor_id, user_id),
  FOREIGN KEY(actor_id) REFERENCES Actor(actor_id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DirectorRating(
  director_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  score INTEGER NOT NULL,
  PRIMARY KEY(director_id, user_id),
  FOREIGN KEY(director_id) REFERENCES Director(director_id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

/* Test Inserts For Now */
INSERT INTO StreamingService(name) VALUES
("Netflix"),
("Hulu"),
("Disney Plus"),
("HBO Max");

INSERT INTO Genre(name) VALUES
("Science Fiction"),
("Romance"),
("Comedy"),
("Fantasy"),
("Adventure"),
("Action");

INSERT INTO Director(name) VALUES
("Steven Spielberg"),
("Christopher Nolan");

INSERT INTO Actor(name) VALUES
("Zooey Deschanel"),
("Leonardo DiCaprio"),
("Joseph Gordon-Levitt"),
("Shailene Woodley");

INSERT INTO Media(name, genre_id, director_id) VALUES
("New Girl", 3, 1),
("Inception", 6, 2);

INSERT INTO ViewableOn(media_id, ss_id) VALUES
(1, 1),
(2, 1),
(2, 4);

INSERT INTO StarsIn(media_id, actor_id) VALUES
(2, 2),
(2, 3);


