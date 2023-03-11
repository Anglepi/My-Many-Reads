CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn TEXT UNIQUE,
    title TEXT NOT NULL,
    synopsis TEXT NOT NULL,
    publisher TEXT NOT NULL,
    publishing_date TEXT NOT NULL,
    edition TEXT NOT NULL
);

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date TEXT NOT NULL
);

CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    genre TEXT NOT NULL
);

CREATE TABLE authored (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books (id),
    author_id INTEGER REFERENCES authors (id)
);

CREATE TABLE book_genres (
    id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books (id),
    genre_id INTEGER REFERENCES genres (id)
);

CREATE TABLE libraries (
    id SERIAL PRIMARY KEY,
    owner TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE TYPE ReadingStatus AS ENUM ('PLAN_TO_READ', 'CURRENTLY_READING', 'COMPLETED', 'DROPPED', 'ON_HOLD', '');

CREATE TABLE library_entries (
    id SERIAL PRIMARY KEY,
    library_id INTEGER REFERENCES libraries (id),
    book_id INTEGER REFERENCES books (id),
    score INTEGER,
    reading_status ReadingStatus NOT NULL DEFAULT ''
);

CREATE TABLE user_recommendations (
    id SERIAL PRIMARY KEY,
    book1_id INTEGER REFERENCES books (id),
    book2_id INTEGER REFERENCES books (id),
    CHECK (book1_id <> book2_id)
);

CREATE TABLE user_recommendation_comments (
    id SERIAL PRIMARY KEY,
    recommendation_id INTEGER REFERENCES user_recommendations (id),
    author TEXT NOT NULL,
    comment TEXT NOT NULL,
    score INTEGER NOT NULL DEFAULT 0
);

insert into genres(genre) values ('Action'), --1
        ('Sci-fi'), --2
        ('Fantasy'), --3
        ('Fiction'), --4
        ('Suspense'), --5
        ('Graphic novel'), --6
        ('Manga'), --7
        ('Historical'), --8
        ('Art'), --9
        ('Science'), --10
        ('Thriller'); --11

insert into books(isbn, title, synopsis, publisher, publishing_date, edition) values
    ('99921-58-10-7', 'A book', 'Some random descriptivie text about the book', 'Nova editorial', '2017-10-28', '1st Edition'),
    ('9971-5-0210-0', 'A book: Reloaded', 'Some random descriptivie text about the book','Nova editorial', '2018-10-28', 'Special anniversary edition'),
    ('0-9752298-0-X', 'A book: Revoluitions', 'Some random descriptivie text about the book', 'Nova editorial', '2019-10-28', '5th edition'),
    ('960-425-059-0', 'Recommendations Paradise', 'Some random descriptivie text about the book','Nova editorial','2019-10-28', '5th edition'),
    ('80-902734-1-6', 'The Spanish Omelette Hero', 'Some random descriptivie text about the book', 'Nova editorial','2019-10-28','5th edition');

insert into book_genres(book_id, genre_id) values (1,1), (1,3), (2,1), (2,3), (3,1), (3,3), (4,3), (4,10), (4,8), (5,7), (5,9), (5,11);

insert into authors(name, birth_date) values ('Cervantes', '1547-09-29'), ('Manuel', '1987-11-13'), ('Ángel Píñar', '1984-01-01');

insert into authored(book_id, author_id) values (1,1), (2,1), (2,2), (3,1), (4,3), (5,3);

insert into libraries(owner, name) values ('user1', 'myLibrary'), ('user1', 'myOtherLibrary'), ('user2', 'generic');

insert into library_entries(library_id, book_id, score, reading_status) values (3, 1, 5, 'COMPLETED');

insert into user_recommendations(book1_id, book2_id) values (1,2), (1,3);

insert into user_recommendation_comments(recommendation_id, author, comment) values (1, 'RandomGuy', 'They are both cool');
