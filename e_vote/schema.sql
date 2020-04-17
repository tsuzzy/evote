DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS election_info;
DROP TABLE IF EXISTS candidate_list;
DROP TABLE IF EXISTS vote;
DROP TABLE IF EXISTS result;

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
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  election_number INTEGER NOT NULL,
  candidate_id INTEGER NOT NULL,
  candidate_name TEXT NOT NULL,
  discription TEXT,
  calcu_id INTEGER NOT NULL,
  FOREIGN KEY (election_number) REFERENCES election_info (info_id),
  FOREIGN KEY (candidate_id) REFERENCES user (user_id),
  FOREIGN KEY (candidate_name) REFERENCES user (realname)
);

CREATE TABLE vote(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  voter_id INTEGER NOT NULL,
  election_number INTEGER NOT NULL,
  num INTEGER NOT NULL,
  FOREIGN KEY (voter_id) REFERENCES user (user_id),
  FOREIGN KEY (election_number) REFERENCES election_info (info_id),
  FOREIGN KEY (num) REFERENCES candidate_list (calcu_id)
);

CREATE TABLE result(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  election_number INTEGER NOT NULL,
  candidate TEXT NOT NULL,
  rate FLOAT NOT NULL,
  FOREIGN KEY (election_number) REFERENCES election_info (info_id),
  FOREIGN KEY (candidate) REFERENCES candidate_list (candidate_name)
);