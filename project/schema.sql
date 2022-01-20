DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Selected;
DROP TABLE IF EXISTS Liked;
DROP TABLE IF EXISTS Posses;
DROP TABLE IF EXISTS Rights;
DROP TABLE IF EXISTS Role;

CREATE TABLE Posts(
   id_post INTEGER PRIMARY KEY AUTOINCREMENT,
   title_post TEXT NOT NULL,
   content_post TEXT NOT NULL,
   created DATE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Events(
   id_event INTEGER PRIMARY KEY AUTOINCREMENT,
   title_event TEXT NOT NULL,
   content_event TEXT,
   event_date DATETIME NOT NULL
);

CREATE TABLE Role(
   id_role INTEGER PRIMARY KEY AUTOINCREMENT,
   role_name TEXT
);

CREATE TABLE Rights(
   id_rights INTEGER PRIMARY KEY AUTOINCREMENT,
   rights_name TEXT
);

CREATE TABLE Users(
   email TEXT,
   name TEXT NOT NULL,
   password TEXT NOT NULL,
   id_role INTEGER NOT NULL,
   PRIMARY KEY(email),
   FOREIGN KEY(id_role) REFERENCES Role(id_role)
);

CREATE TABLE Selected(
   email TEXT,
   id_event INTEGER,
   PRIMARY KEY(email, id_event),
   FOREIGN KEY(email) REFERENCES Users(email),
   FOREIGN KEY(id_event) REFERENCES Events(id_event)
);

CREATE TABLE Liked(
   email TEXT,
   id_post INTEGER,
   PRIMARY KEY(email, id_post),
   FOREIGN KEY(email) REFERENCES Users(email),
   FOREIGN KEY(id_post) REFERENCES Posts(id_post)
);

CREATE TABLE posses(
   id_role INTEGER,
   id_rights INTEGER,
   PRIMARY KEY(id_role, id_rights),
   FOREIGN KEY(id_role) REFERENCES Role(id_role),
   FOREIGN KEY(id_rights) REFERENCES Rights(id_rights)
);


