DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS bugs;
DROP TABLE IF EXISTS commits;
DROP TABLE IF EXISTS commits_files;
DROP TABLE IF EXISTS commits_parents;

CREATE TABLE bugs (
    bug_id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    status VARCHAR(64),
    owner VARCHAR(128),
    closed_on DATETIME,
    type VARCHAR(64),
    priority INTEGER,
    component VARCHAR(128),
    stars INTEGER,
    reported_by VARCHAR(128),
    opened_date DATETIME,
    description TEXT
);

CREATE TABLE comments (
    bug_id INTEGER REFERENCES bugs(bug_id),
    author VARCHAR(128),
    comment_date DATETIME,
    what TEXT
);

CREATE TABLE commits (
    commit_hash VARCHAR(255) PRIMARY KEY,
    tree_hash VARCHAR(255),
    project VARCHAR(255),
    author VARCHAR(255),
    commit_date DATETIME,
    tz INTEGER,
    subject VARCHAR(255),
    message TEXT,
    bug_id INTEGER
);

CREATE TABLE commits_files (
    commit_hash VARCHAR(255) REFERENCES commits(commit_hash),
    commit_date DATETIME,
    file VARCHAR(255)
);

CREATE TABLE commits_parents (
    commit_hash VARCHAR(255) REFERENCES commits(commit_hash),
    parent_hash VARCHAR(255)
);
