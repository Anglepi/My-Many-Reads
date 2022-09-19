from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Book:
    id: str
    title: str
    synopsis: str
    author: str
    genres: list[Book.Genre]
    publisher: str
    publishing_date: str

    def fromList(books):
        bookList: list[Book] = []
        for book in books:
            bookList.append(Book.fromDict(book))
        return bookList

    def fromDict(book):
        return Book(book["id"], book["title"], book["synopsis"], book["author"], book["genres"], book["publisher"], book["publishing_date"])

    def toDict(self) -> dict:
        return {"id": self.id, "title": self.title, "synopsis": self.synopsis, "author": self.author, "genres": self.genres, "publisher": self.publisher, "publishing_date": self.publishing_date}

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
