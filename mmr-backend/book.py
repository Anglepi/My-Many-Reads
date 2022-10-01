from __future__ import annotations
from dataclasses import asdict, dataclass
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
        return map(lambda book: Book.from_dict(book), books)

    def from_dict(book):
        return Book(**book)

    def to_dict(self):
        return asdict(self)

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
