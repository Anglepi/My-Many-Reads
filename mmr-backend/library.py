from __future__ import annotations
from enum import Enum
from typing import Optional

from book import Book


class Library:
    def __init__(self, owner: str, name: str, entries: list[Library.Entry]) -> None:
        self.__owner: str = owner
        self.__name: str = name
        self.__entries: list[Library.Entry] = entries

    class ReadingStatus(Enum):
        PLAN_TO_READ = "PLAN TO READ"
        CURRENTLY_READING = "CURRENTLY READING"
        COMPLETED = "COMPLETED"
        DROPPED = "DROPPED"
        ON_HOLD = "ON HOLD"

    def to_dict(self) -> dict:
        props = {key.split("__")[-1]: value for (key,
                                                 value) in self.__dict__.items()}
        props["entries"] = Library.Entry.entries_to_dict(props["entries"])
        return props

    @staticmethod
    def from_dict(library_data: dict) -> Library:
        return Library(**library_data)

    class Entry:
        def __init__(self, book: Book, score: Optional[int] = None, status: Optional[Library.ReadingStatus] = None) -> None:
            self.__book: Book = book
            self.__score: Optional[int] = score
            self.__status: Optional[Library.ReadingStatus] = status

        def get_book_id(self) -> str:
            return self.__book.isbn

        def to_dict(self) -> dict:
            return {"book": self.__book.to_dict(), "score": self.__score, "status": self.__status}

        def is_read(self) -> bool:
            return self.__status != Library.ReadingStatus.PLAN_TO_READ

        @staticmethod
        def entries_to_dict(entries: list[Library.Entry]) -> list[dict]:
            return list(map(Library.Entry.to_dict, entries))

    def get_owner(self) -> str:
        return self.__owner

    def get_name(self) -> str:
        return self.__name

    def set_name(self, new_name: str) -> None:
        self.__name = new_name

    def add_entry(self, entry: Library.Entry) -> None:
        self.__entries.append(entry)

    def update_entry(self, book_id: str, new_entry: Library.Entry) -> None:
        for index, entry in enumerate(self.__entries):
            if (entry.get_book_id() == book_id):
                self.__entries[index] = new_entry
                break

    def remove_entry(self, book_id: str) -> None:
        for entry in self.__entries:
            if (entry.get_book_id() == book_id):
                self.__entries.remove(entry)

    def get_entries(self) -> list[Library.Entry]:
        return self.__entries

    def has_book(self, book: Book) -> bool:
        for entry in self.__entries:
            if (entry.get_book_id() == book.isbn):
                return True
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Library):
            return NotImplemented
        return self.__name == other.__name and self.__owner == other.__owner
