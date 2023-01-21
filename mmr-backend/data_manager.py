import json
from book import Book
from library import Library
from user_recommendation import UserRecommendation
from typing import Iterable, Optional, Union


class DataManager:
    def __init__(self, address: str) -> None:
        self._address = address

    def __connect(self) -> None:
        self.connection = open(self._address)

        # Set up fake data until real database is implemented
        if not hasattr(self, 'fake_books'):
            self.fake_books = json.load(self.connection)
        if not hasattr(self, 'fake_libraries'):
            self.fake_libraries = [Library("user1", "myLibrary", list()), Library(
                "user1", "myOtherLibrary", list()), Library("user2", "generic", [Library.Entry(Book.from_dict(self.fake_books[0]), 5, Library.ReadingStatus.COMPLETED)])]
        if not hasattr(self, 'fake_recommendations'):
            self.fake_recommendations = [UserRecommendation(
                (Book.from_dict(self.fake_books[0]).ISBN, Book.from_dict(self.fake_books[1]).ISBN), UserRecommendation.UserComment("Recommender", "first book is similar to second book")),
                UserRecommendation(
                (Book.from_dict(self.fake_books[0]).ISBN, Book.from_dict(self.fake_books[2]).ISBN), UserRecommendation.UserComment("Recommender", "first book is similar to third book"))]
            self.fake_recommendations[0].add_comment(
                UserRecommendation.UserComment("RandomGuy", "They are both cool"))

    def __disconnect(self) -> None:
        if self.connection:
            self.connection.close()

    # BOOKS

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

    # LIBRARIES

    def get_libraries_from_user(self, user: str) -> list[dict]:
        self.__connect()
        # To be replaced by an actual query
        libraries_from_user = filter(
            lambda lib: lib.get_owner() == user, self.fake_libraries)
        self.__disconnect()
        return list(map(lambda lib: lib.to_dict(), libraries_from_user)) if libraries_from_user else []

    def get_library(self, user: str, library_name: str) -> Optional[Library]:
        self.__connect()
        # To be replaced by an actual query
        occurrencies = list(filter(lambda lib: lib.get_owner(
        ) == user and lib.get_name() == library_name, self.fake_libraries))
        self.__disconnect()
        return occurrencies[0] if len(occurrencies) else None

    def delete_library(self, user: str, library_name: str) -> None:
        self.__connect()
        # To be replaced by an actual query
        library: Optional[Library] = self.get_library(user, library_name)
        if library:
            self.fake_libraries.remove(library)
        self.__disconnect()

    def rename_library(self, user: str, library_name: str, new_name: str) -> None:
        self.__connect()
        # To be replaced by an actual query
        library: Optional[Library] = self.get_library(user, library_name)
        if library:
            library.set_name(new_name)
        self.__disconnect()

    def create_library(self, user: str, library_name: str) -> None:
        self.__connect()
        # To be replaced by an actual query
        self.fake_libraries.append(Library(user, library_name, list()))
        self.__disconnect()

    def remove_library_entry(self, user: str, library_name: str, isbn: str) -> None:
        self.__connect()
        # To be replaced by an actual query
        library: Optional[Library] = self.get_library(user, library_name)
        if library:
            library.remove_entry(isbn)
        self.__disconnect()

    def add_library_entry(self, user: str, library_name: str, isbn: str) -> bool:
        self.__connect()
        # To be replaced by an actual query
        book: Optional[Book] = self.get_book(isbn)
        library: Optional[Library] = self.get_library(user, library_name)
        self.__disconnect()

        if book and library:
            library.add_entry(Library.Entry(book))
        return bool(book and library)

    def update_library_entry(self, user: str, library_name: str, isbn: str, score: int, status: Library.ReadingStatus) -> None:
        self.__connect()
        # To be replaced by an actual query
        book: Optional[Book] = self.get_book(isbn)
        library: Optional[Library] = self.get_library(user, library_name)
        self.__disconnect()

        if book and library:
            library.update_entry(isbn, Library.Entry(book, score, status))

    # RECOMMENDATIONS

    def get_recommendations_for_book(self, isbn: str) -> list[dict]:
        self.__connect()
        # To be replaced by an actual query
        recommendations_for_book: Iterable[UserRecommendation] = filter(
            lambda recommendation: recommendation.has_book(isbn), self.fake_recommendations)
        self.__disconnect()
        return list(map(lambda recommendation: recommendation.to_dict(), recommendations_for_book))

    def create_user_recommendation(self, isbn1: str, isbn2: str, user: str, comment: str) -> bool:
        self.__connect()
        book1: Optional[Book] = self.get_book(isbn1)
        book2: Optional[Book] = self.get_book(isbn2)

        if not (book1 and book2):
            self.__disconnect()
            return False

        recommendations: list[UserRecommendation] = list(filter(lambda recommendation: recommendation.has_book(
            isbn1) and recommendation.has_book(isbn2), self.fake_recommendations))

        if len(recommendations):
            recommendations[0].add_comment(
                UserRecommendation.UserComment(user, comment))
        else:
            self.fake_recommendations.append(UserRecommendation(
                (isbn1, isbn2), UserRecommendation.UserComment(user, comment)))
        return True
