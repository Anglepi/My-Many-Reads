from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Book:
    ISBN: str
    title: str
    synopsis: str
    author: list[str]
    genres: list[Book.Genre]
    publisher: str
    publishing_date: str
    edition: str

    def from_list(books):
        bookList: list[Book] = []
        for book in books:
            bookList.append(Book.from_dict(book))
        return bookList

    def from_dict(book):
        return Book(book["ISBN"], book["title"], book["synopsis"], book["author"], book["genres"], book["publisher"], book["publishing_date"], book["edition"])

    def to_dict(self) -> dict:
        return {"ISBN": self.ISBN, "title": self.title, "synopsis": self.synopsis, "author": self.author, "genres": self.genres, "publisher": self.publisher, "publishing_date": self.publishing_date, "edition": self.edition}

    class Genre(Enum):
        ACTION = "Action"
        SCIFI = "Sci-fi"
        FANTASY = "Fantasy"
        FICTION = "Fiction"
        SUSPENSE = "Suspense"
        GRAPHIC_NOVEL = "Graphic novel"
        MANGA = "Manga"
        HISTORICAL = "Historical"
        ART = "Art"
        SCIENCE = "Science"
        THRILLER = "Thriller"
