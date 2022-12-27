from __future__ import annotations
from dataclasses import asdict, dataclass
from enum import Enum


@dataclass(frozen=True)
class Book:
    ISBN: str
    title: str
    synopsis: str
    authors: list[str]
    genres: list[Book.Genre]
    publisher: str
    publishing_date: str
    edition: str

    @staticmethod
    def from_list(books: list[dict]) -> list[Book]:
        return list(map(lambda book: Book.from_dict(book), books))

    @staticmethod
    def from_dict(book: dict) -> Book:
        return Book(**book)

    def to_dict(self) -> dict:
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
