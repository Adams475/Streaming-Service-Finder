
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  firstname TEXT PRIMARY KEY NOT NULL,
	lastname TEXT NOT NULL
);

INSERT INTO users(firstname, lastname) VALUES
("Colston", "Streit"),
("Nick", "Johnson");