from __future__ import annotations
from dataclasses import asdict, dataclass
from enum import Enum
import re


@dataclass(frozen=True)
class Book:
    isbn: str
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
        Book.validate_isbn(book["isbn"])
        return Book(**book)

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        isbn_code: str = re.sub('\D', '', isbn)
        is_valid: bool = False
        if isbn[-1] == 'X':
            isbn_code += 'X'

        if (len(isbn_code) == 10):
            is_valid = Book.__validate_isbn_10(isbn_code)
        elif (len(isbn_code) == 13):
            is_valid = Book.__validate_isbn_13(isbn_code)

        if is_valid:
            return True

        raise Exception("Malformed ISBN")

    @staticmethod
    def __validate_isbn_10(isbn: str) -> bool:
        sum: int = 0
        for i in range(10):
            current_number: int = 10 if isbn[i] == 'X' else int(isbn[i])
            sum += current_number * (10-i)

        return not bool(sum % 11)

    @staticmethod
    def __validate_isbn_13(isbn: str) -> bool:
        sum: int = 0

        for i in range(0, 12, 2):
            sum += 10 if isbn[i] == 'X' else int(isbn[i])
        for i in range(1, 12, 2):
            current_number: int = 10 if isbn[i] == 'X' else int(isbn[i])
            sum += current_number * 3

        return not bool(sum % 10)

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
