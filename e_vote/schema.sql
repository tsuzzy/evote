DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS election_info;
DROP TABLE IF EXISTS candidate_list;

CREATE TABLE user(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  user_id INTEGER UNIQUE NOT NULL,
  realname TEXT NOT NULL
);

CREATE TABLE admin(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  admin_id INTEGER UNIQUE NOT NULL,
  realname TEXT NOT NULL
);

CREATE TABLE election_info(
  info_id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES admin (admin_id)
);

CREATE TABLE candidate_list(
  candidate_id INTEGER PRIMARY KEY NOT NULL,
  candidate_name TEXT NOT NULL,
  discription TEXT NOT NULL,
  FOREIGN KEY (candidate_id) REFERENCES user (user_id),
  FOREIGN KEY (candidate_name) REFERENCES user(realname)
);