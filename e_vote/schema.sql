DROP TABLE IF EXISTS voter;
DROP TABLE IF EXISTS candidate;
DROP TABLE IF EXISTS election_authority;
DROP TABLE IF EXISTS system_authority;
DROP TABLE IF EXISTS candidate_list;
DROP TABLE IF EXISTS voter_list;

CREATE TABLE voter(
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  vid INTEGER PRIMARY KEY UNIQUE NOT NULL,
  vname TEXT NOT NULL
);

CREATE TABLE candidate(
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  cid INTEGER PRIMARY KEY UNIQUE NOT NULL,
  cname TEXT NOT NULL
);

CREATE TABLE election_authority(
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  EAid INTEGER PRIMARY KEY UNIQUE NOT NULL,
  EAname TEXT NOT NULL
);

CREATE TABLE system_authority(
  vip_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
  vip_psw TEXT NOT NULL
);

CREATE TABLE candidate_list(
  candidate_id INTEGER PRIMARY KEY NOT NULL,
  candidate_name TEXT NOT NULL,
  FOREIGN KEY (candidate_id) REFERENCES candidate (cid)
);

CREATE TABLE voter_list(
  voter_id INTEGER PRIMARY KEY NOT NULL,
  FOREIGN KEY (voter_id) REFERENCES voter (vid)
);