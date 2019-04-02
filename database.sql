-- Table for user: 1. id, username, password
CREATE TABLE user_book (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR NOT NULL,
    user_password VARCHAR NOT NULL
);
--user test: user_name: alit, user_password: si
INSERT INTO user_book (user_name, user_password) VALUES ('alit', 'si');

-- Table for books
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

-- Table for smaller books
CREATE TABLE smaller_books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);
