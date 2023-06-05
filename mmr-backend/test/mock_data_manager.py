from __future__ import annotations
import json
from book import Book
from library import Library
from user_recommendation import UserRecommendation
from typing import Iterable, Optional
import os

current_dir = os.path.dirname(__file__)
sample_data_path = "sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)


class DataManager:
    def __init__(self) -> None:
        # Set up fake data until real database is implemented
        books_data = open(data_path)
        self.fake_books = json.load(books_data)
        books_data.close()
        self.fake_libraries = [Library("user1", "myLibrary", list()), Library(
            "user1", "myOtherLibrary", list()), Library("user2", "generic", [Library.Entry(Book.from_dict(self.fake_books[0]), 5, Library.ReadingStatus.COMPLETED)])]
        self.fake_recommendations = [UserRecommendation(
            (Book.from_dict(self.fake_books[0]).id, Book.from_dict(self.fake_books[1]).id), UserRecommendation.UserComment("RandomGuy", "They are both cool")),
            UserRecommendation(
            (Book.from_dict(self.fake_books[0]).id, Book.from_dict(self.fake_books[2]).id), UserRecommendation.UserComment("OtherGuy", "They are both entertaining"))]

    # BOOKS

    def get_books(self) -> list[Book]:
        # To be replaced by an actual query
        books = self.fake_books
        return Book.from_list(books)

    def get_book(self, id: int) -> Optional[Book]:
        # To be replaced by an actual query
        occurrencies = list(filter(lambda book: book.to_dict()[
            "id"] == id, Book.from_list(self.fake_books)))
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

    def create_library(self, user: str, library_name: str) -> bool:
        # To be replaced by an actual query
        for library in self.fake_libraries:
            if library.get_owner() == user and library.get_name() == library_name:
                return False
        self.fake_libraries.append(Library(user, library_name, list()))
        return True

    def remove_library_entry(self, user: str, library_name: str, book_id: int) -> None:
        # To be replaced by an actual query
        library: Optional[Library] = self.get_library(user, library_name)
        if library:
            library.remove_entry(book_id)

    def add_library_entry(self, user: str, library_name: str, book_id: int) -> bool:
        # To be replaced by an actual query
        book: Optional[Book] = self.get_book(book_id)
        library: Optional[Library] = self.get_library(user, library_name)
        if book and library:
            for entry in library.get_entries():
                if entry.get_book_id() == book_id:
                    return False
            library.add_entry(Library.Entry(book, None, ""))
        return bool(book and library)

    def update_library_entry(self, user: str, library_name: str, book_id: int, score: int, status: Library.ReadingStatus) -> None:
        # To be replaced by an actual query
        book: Optional[Book] = self.get_book(book_id)
        library: Optional[Library] = self.get_library(user, library_name)
        if book and library:
            library.update_entry(book_id, Library.Entry(book, score, status))

    # RECOMMENDATIONS

    def get_recommendations_for_book(self, book_id: int) -> list[dict]:
        # To be replaced by an actual query
        recommendations_for_book: Iterable[UserRecommendation] = filter(
            lambda recommendation: recommendation.has_book(book_id), self.fake_recommendations)
        return list(map(lambda recommendation: recommendation.to_dict(), recommendations_for_book))

    def create_user_recommendation(self, book_id1: int, book_id2: int, user: str, comment: str) -> bool:
        book1: Optional[Book] = self.get_book(book_id1)
        book2: Optional[Book] = self.get_book(book_id2)

        if not (book1 and book2):
            return 404

        recommendations: list[UserRecommendation] = list(filter(lambda recommendation: recommendation.has_book(
            book_id1) and recommendation.has_book(book_id2), self.fake_recommendations))

        if len(recommendations):
            for recommendation in recommendations:
                if len(recommendation.get_author_comments(user)) > 0:
                    return 409
            recommendations[0].add_comment(
                UserRecommendation.UserComment(user, comment))
        else:
            self.fake_recommendations.append(UserRecommendation(
                (book_id1, book_id2), UserRecommendation.UserComment(user, comment)))
        return 201

    def vote_user_recommendation(self, book_id1: int, book_id2: int, user: str) -> bool:
        book1: Optional[Book] = self.get_book(book_id1)
        book2: Optional[Book] = self.get_book(book_id2)

        if not (book1 and book2):
            return False

        recommendations: list[UserRecommendation] = list(filter(lambda recommendation: recommendation.has_book(
            book_id1) and recommendation.has_book(book_id2) and len(recommendation.get_author_comments(user)), self.fake_recommendations))

        if len(recommendations):
            recommendations[0].vote_comment(user)
            return True

        return False

    def get_book_stats(self, book_id: int) -> dict:
        return {"title": "A book", "score": 5.0, "views": 1, "readers": 1} if book_id == 1 else None

    def get_genres_stats(self) -> dict:
        return [{'genre': 'Action', 'views': 1, 'score': 5.0, 'readers': 1},
                {'genre': 'Fantasy', 'views': 1,
                 'score': 5.0, 'readers': 1},
                {'genre': 'Manga', 'views': 0, 'score': 0, 'readers': 0},
                {'genre': 'Science', 'views': 0,
                 'score': 0, 'readers': 0},
                {'genre': 'Thriller', 'views': 0,
                 'score': 0, 'readers': 0},
                {'genre': 'Historical', 'views': 0,
                 'score': 0, 'readers': 0},
                {'genre': 'Art', 'views': 0, 'score': 0, 'readers': 0}]
