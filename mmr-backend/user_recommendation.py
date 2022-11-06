from __future__ import annotations
from typing import Tuple


class UserRecommendation:
    def __init__(self, books: Tuple[str, str], user_comment: UserRecommendation.UserComment) -> None:
        self.__books = sorted(books)
        self.__comments = [user_comment]

    class UserComment:
        def __init__(self, user: str, comment: str):
            self.__user = user
            self.__comment = comment
            self.__score = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserRecommendation):
            return NotImplemented
        return self.__books == other.__books
