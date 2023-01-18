import json
from book import Book
from library import Library
from typing import Optional


class DataManager:
    def __init__(self, address: str) -> None:
        self._address = address

    def __connect(self) -> None:
        self.connection = open(self._address)

        # Set up fake data until real database is implemented
        self.fake_books = json.load(self.connection)
        self.fake_libraries = [Library("user1", "myLibrary", list()), Library(
            "user1", "myOtherLibrary", list()), Library("user2", "generic", [Library.Entry(self.fake_books[0], 5, Library.ReadingStatus.COMPLETED)])]

    def __disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            del self.fake_books
            del self.fake_libraries

    def get_books(self) -> list[Book]:
        self.__connect()
        # To be replaced by an actual query
        books = self.fake_books
        self.__disconnect()
        return Book.from_list(books)

    def get_book(self, isbn: str) -> Optional[Book]:
        self.__connect()
        # To be replaced by an actual query
        occurrencies = list(filter(lambda book: book.to_dict()[
            "ISBN"] == isbn, Book.from_list(self.fake_books)))
        self.__disconnect()
        return occurrencies[0] if len(occurrencies) else None
