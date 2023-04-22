from __future__ import annotations
from typing import Tuple


class UserRecommendation:
    def __init__(self, books: Tuple[str, str], user_comment: UserRecommendation.UserComment) -> None:
        self.__books = sorted(books)
        self.__comments = [user_comment]

    class UserComment:
        def __init__(self, user: str, comment: str, score: int = 0):
            self.__author = user
            self.__comment = comment
            self.__score = score

        def get_author(self) -> str:
            return self.__author

        def to_dict(self) -> dict:
            return {"author": self.__author, "comment": self.__comment, "score": self.__score}

        def vote(self) -> None:
            self.__score += 1

        @staticmethod
        def entries_to_dict(entries: list[UserRecommendation.UserComment]) -> list[dict]:
            return list(map(UserRecommendation.UserComment.to_dict, entries))

    def vote_comment(self, author: str) -> None:
        comments = self.get_author_comments(author)

        if len(comments):
            comments[0].vote()

    def get_author_comments(self, author: str) -> list[UserComment]:
        return list(
            filter(lambda current_comment: current_comment.get_author() == author, self.__comments))

    def has_book(self, isbn: str) -> bool:
        return isbn in self.__books

    def add_comment(self, comment: UserComment) -> None:
        occurrences = list(
            filter(lambda current_comment: current_comment.get_author() == comment.get_author(), self.__comments))
        if not len(occurrences):
            self.__comments.append(comment)

    def to_dict(self) -> dict:
        return {"books": self.__books, "comments": UserRecommendation.UserComment.entries_to_dict(self.__comments)}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserRecommendation):
            return NotImplemented
        return self.__books == other.__books
