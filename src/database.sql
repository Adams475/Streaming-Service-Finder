SET FOREIGN_KEY_CHECKS=0;

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

CREATE TABLE StreamingService(
  ss_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(64) NOT NULL
);
CREATE UNIQUE Index StreamingService_Index ON StreamingService((LOWER(name))) USING BTREE;

CREATE TABLE Genre(
  genre_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  description VARCHAR(1024) DEFAULT '' NOT NULL
);
CREATE UNIQUE INDEX Genre_Index ON Genre((LOWER(name))) USING BTREE;

CREATE TABLE Director(
  director_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  sex VARCHAR(16) DEFAULT 'Unspecified' NOT NULL,
  birthDate VARCHAR(16) DEFAULT '?' NOT NULL
);
CREATE UNIQUE INDEX Director_Index ON Director((LOWER(name))) USING BTREE;

CREATE TABLE Actor(
  actor_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  sex VARCHAR(16) DEFAULT 'Unspecified' NOT NULL,
  birthDate VARCHAR(16) DEFAULT '?' NOT NULL
);
CREATE UNIQUE INDEX Actor_Index ON Actor((LOWER(name))) USING BTREE;

CREATE TABLE User(
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(64) NOT NULL,
  hashedPassword VARCHAR(128) NOT NULL
);
CREATE UNIQUE INDEX User_Index ON User(username) USING BTREE;

CREATE TABLE Media(
  media_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(64) NOT NULL,
  releaseYear INT DEFAULT -1 NOT NULL,
  genre_id INT NOT NULL,
  director_id INT NOT NULL,
  FOREIGN KEY(genre_id) REFERENCES Genre(genre_id),
  FOREIGN KEY(director_id) REFERENCES Director(director_id)
);
CREATE UNIQUE INDEX Media_Index ON Media((LOWER(name))) USING BTREE;

CREATE TABLE ViewableOn(
  media_id INT NOT NULL,
  ss_id INT NOT NULL,
  PRIMARY KEY(media_id, ss_id),
  FOREIGN KEY(media_id) REFERENCES Media(media_id) ON DELETE CASCADE,
  FOREIGN KEY(ss_id) REFERENCES StreamingService(ss_id) ON DELETE CASCADE
);

CREATE TABLE StarsIn(
  actor_id INT NOT NULL,
  media_id INT NOT NULL,
  PRIMARY KEY(actor_id, media_id),
  FOREIGN KEY(actor_id) REFERENCES Actor(actor_id) ON DELETE CASCADE,
  FOREIGN KEY(media_id) REFERENCES Media(media_id) ON DELETE CASCADE
);

CREATE TABLE MediaRating(
  media_id INT NOT NULL,
  user_id INT NOT NULL,
  score INT NOT NULL,
  PRIMARY KEY(media_id, user_id),
  FOREIGN KEY(media_id) REFERENCES Media(media_id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE ActorRating(
  actor_id INT NOT NULL,
  user_id INT NOT NULL,
  score INT NOT NULL,
  PRIMARY KEY(actor_id, user_id),
  FOREIGN KEY(actor_id) REFERENCES Actor(actor_id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE DirectorRating(
  director_id INT NOT NULL,
  user_id INT NOT NULL,
  score INT NOT NULL,
  PRIMARY KEY(director_id, user_id),
  FOREIGN KEY(director_id) REFERENCES Director(director_id) ON DELETE CASCADE,
  FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

SET FOREIGN_KEY_CHECKS=1;
