--
-- File generated with SQLiteStudio v3.4.3 on mar. ago. 13 19:25:25 2024
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: AccessToken
CREATE TABLE IF NOT EXISTS AccessToken (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT    NOT NULL,
    accesstoken TEXT    NOT NULL,
    issuedate   TEXT    NOT NULL,
    revokedate  TEXT,
    FOREIGN KEY (
        username
    )
    REFERENCES User (username) 
);


-- Table: Operation
CREATE TABLE IF NOT EXISTS Operation (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT    CHECK (type IN ('addition', 'subtraction', 'multiplication', 'division', 'square_root', 'random_string') ) 
                 NOT NULL,
    cost REAL    NOT NULL
);


-- Table: Record
CREATE TABLE IF NOT EXISTS Record (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_id       INTEGER NOT NULL,
    user_id            INTEGER NOT NULL,
    amount             REAL    NOT NULL,
    user_balance       REAL    NOT NULL,
    operation_response TEXT    NOT NULL,
    date               TEXT    NOT NULL,
    deleted_at         TEXT,
    FOREIGN KEY (
        operation_id
    )
    REFERENCES Operation (id),
    FOREIGN KEY (
        user_id
    )
    REFERENCES User (id) 
);


-- Table: User
CREATE TABLE IF NOT EXISTS User (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    NOT NULL
                     UNIQUE,-- Email como username
    password TEXT    NOT NULL,
    status   TEXT    CHECK (status IN ('active', 'inactive') ) 
                     NOT NULL
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
