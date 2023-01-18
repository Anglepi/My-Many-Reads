import json
from book import Book
from typing import Optional


class DataManager:
    def __init__(self, address: str) -> None:
        self._address = address

    def __connect(self) -> None:
        self.connection = open(self._address)

    def __disconnect(self) -> None:
        if self.connection:
            self.connection.close()

    def get_books(self) -> list[Book]:
        self.__connect()
        books_data = json.load(self.connection)
        self.__disconnect()
        return Book.from_list(books_data)

    def get_book(self, isbn: str) -> Optional[Book]:
        # To be replaced by an actual query
        books: list[Book] = self.get_books()
        occurrencies = list(filter(lambda book: book.to_dict()[
            "ISBN"] == isbn, books))
        return occurrencies[0] if len(occurrencies) else None
