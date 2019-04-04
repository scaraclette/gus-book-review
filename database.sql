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

-- Table for smaller books (testing purposes)
CREATE TABLE smaller_books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL
);

-- Table for reviews
CREATE TABLE user_reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_book,
    book_id INTEGER REFERENCES books,
    rating REAL NOT NULL,
    review VARCHAR NOT NULL
);

/*
    id      user_id             book_id         rating      review
    1       *book_user id*      *books id*      ...         ...

*/

--Join query example
SELECT * FROM user_reviews JOIN user_book on user_reviews.user_id=user_book.id;

-- Want: user_reviews joined with user_book for specific book
SELECT * FROM user_reviews JOIN user_book ON user_reviews.user_id=user_book.id AND user_reviews.book_id = 1;
