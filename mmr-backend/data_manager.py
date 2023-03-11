from __future__ import annotations
import json
from book import Book
from library import Library
from user_recommendation import UserRecommendation
from typing import Iterable, Optional


class DataManager:
    def __init__(self, address: str) -> None:
        self._address = address

        # Set up fake data until real database is implemented
        books_data = open(self._address)
        self.fake_books = json.load(books_data)
        books_data.close()
        self.fake_libraries = [Library("user1", "myLibrary", list()), Library(
            "user1", "myOtherLibrary", list()), Library("user2", "generic", [Library.Entry(Book.from_dict(self.fake_books[0]), 5, Library.ReadingStatus.COMPLETED)])]
        self.fake_recommendations = [UserRecommendation(
            (Book.from_dict(self.fake_books[0]).isbn, Book.from_dict(self.fake_books[1]).isbn), UserRecommendation.UserComment("Recommender", "first book is similar to second book")),
            UserRecommendation(
            (Book.from_dict(self.fake_books[0]).isbn, Book.from_dict(self.fake_books[2]).isbn), UserRecommendation.UserComment("Recommender", "first book is similar to third book"))]
        self.fake_recommendations[0].add_comment(
            UserRecommendation.UserComment("RandomGuy", "They are both cool"))

    # BOOKS

    def get_books(self) -> list[Book]:
        # To be replaced by an actual query
        books = self.fake_books
        return Book.from_list(books)

    def get_book(self, isbn: str) -> Optional[Book]:
        # To be replaced by an actual query
        occurrencies = list(filter(lambda book: book.to_dict()[
            "isbn"] == isbn, Book.from_list(self.fake_books)))
        return occurrencies[0] if len(occurrencies) else None

    # LIBRARIES

    def get_libraries_from_user(self, user: str) -> list[dict]:
        # To be replaced by an actual query
        libraries_from_user = filter(
            lambda lib: lib.get_owner() == user, self.fake_libraries)
        return list(map(lambda lib: lib.to_dict(), libraries_from_user)) if libraries_from_user else []

    def get_library(self, user: str, library_name: str) -> Optional[Library]:
        # To be replaced by an actual query
        occurrencies = list(filter(lambda lib: lib.get_owner(
        ) == user and lib.get_name() == library_name, self.fake_libraries))
        return occurrencies[0] if len(occurrencies) else None

    def delete_library(self, user: str, library_name: str) -> None:
        # To be replaced by an actual query
        library: Optional[Library] = self.get_library(user, library_name)
        if library:
            self.fake_libraries.remove(library)

    def rename_library(self, user: str, library_name: str, new_name: str) -> None:
        # To be replaced by an actual query
        library: Optional[Library] = self.get_library(user, library_name)
        if library:
            library.set_name(new_name)

    def create_library(self, user: str, library_name: str) -> None:
        # To be replaced by an actual query
        self.fake_libraries.append(Library(user, library_name, list()))

    def remove_library_entry(self, user: str, library_name: str, isbn: str) -> None:
        # To be replaced by an actual query
        library: Optional[Library] = self.get_library(user, library_name)
        if library:
            library.remove_entry(isbn)

    def add_library_entry(self, user: str, library_name: str, isbn: str) -> bool:
        # To be replaced by an actual query
        book: Optional[Book] = self.get_book(isbn)
        library: Optional[Library] = self.get_library(user, library_name)
        if book and library:
            library.add_entry(Library.Entry(book))
        return bool(book and library)

    def update_library_entry(self, user: str, library_name: str, isbn: str, score: int, status: Library.ReadingStatus) -> None:
        # To be replaced by an actual query
        book: Optional[Book] = self.get_book(isbn)
        library: Optional[Library] = self.get_library(user, library_name)
        if book and library:
            library.update_entry(isbn, Library.Entry(book, score, status))

    # RECOMMENDATIONS

    def get_recommendations_for_book(self, isbn: str) -> list[dict]:
        # To be replaced by an actual query
        recommendations_for_book: Iterable[UserRecommendation] = filter(
            lambda recommendation: recommendation.has_book(isbn), self.fake_recommendations)
        return list(map(lambda recommendation: recommendation.to_dict(), recommendations_for_book))

    def create_user_recommendation(self, isbn1: str, isbn2: str, user: str, comment: str) -> bool:
        book1: Optional[Book] = self.get_book(isbn1)
        book2: Optional[Book] = self.get_book(isbn2)
        if not (book1 and book2):
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

    def vote_user_recommendation(self, isbn1: str, isbn2: str, user: str) -> bool:
        book1: Optional[Book] = self.get_book(isbn1)
        book2: Optional[Book] = self.get_book(isbn2)

        if not (book1 and book2):
            return False

        recommendations: list[UserRecommendation] = list(filter(lambda recommendation: recommendation.has_book(
            isbn1) and recommendation.has_book(isbn2) and len(recommendation.get_author_comments(user)), self.fake_recommendations))

        if len(recommendations):
            recommendations[0].vote_comment(user)
            return True

        return False
