from __future__ import annotations
from typing import Tuple


class UserRecommendation:
    def __init__(self, books: Tuple[str, str], user_comment: UserRecommendation.UserComment) -> None:
        self.__books = sorted(books)
        self.__comments = [user_comment]

    class UserComment:
        def __init__(self, user: str, comment: str):
            self.__author = user
            self.__comment = comment
            self.__score = 0

        def to_dict(self) -> dict:
            return {"author": self.__author, "comment": self.__comment, "score": self.__score}

        @staticmethod
        def entries_to_dict(entries: list[UserRecommendation.UserComment]) -> list[dict]:
            return list(map(UserRecommendation.UserComment.to_dict, entries))

    def add_comment(self, comment: UserComment) -> None:
        self.__comments.append(comment)

    def to_dict(self) -> dict:
        return {"books": self.__books, "comments": UserRecommendation.UserComment.entries_to_dict(self.__comments)}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserRecommendation):
            return NotImplemented
        return self.__books == other.__books
