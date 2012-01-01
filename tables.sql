DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS bugs;

CREATE TABLE bugs (
    bug_id INTEGER PRIMARY KEY,
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


