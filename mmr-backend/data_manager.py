import json
from book import Book


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
