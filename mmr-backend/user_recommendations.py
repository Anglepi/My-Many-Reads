from __future__ import annotations
from typing import Tuple


class UserRecommendation:
    def __init__(self, books: Tuple[str, str], user_comment: UserRecommendation.UserComment) -> None:
        self.__books = sorted(books)

    class UserComment:
        def __init__(self, user: str, comment: str):
            self.__user = user
            self.__comment = comment
            self.__score = 0
