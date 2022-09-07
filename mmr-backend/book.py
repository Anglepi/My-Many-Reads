from __future__ import annotations
from enum import Enum


class Book:
    def __init__(self, id: str, title: str, synopsis: str, author: str, genres: list[Book.Genre], publisher: str, publishing_date: str):
        self.__id: str = id
        self.__title: str = title
        self.__synopsis: str = synopsis
        self.__author: str = author
        self.__genres: list[Book.Genre] = genres
        self.__publisher: str = publisher
        self.__publishing_date: str = publishing_date

    class Genre(Enum):
        ACTION = "Action"
        SCIFI = "Sci-fi"
        FANTASY = "Fantasy"
        FICTION = "Fiction"
        SUSPENSE = "Suspense"
        GRAPHIC_NOVEL = "Graphic novel"
        MANGA = "Manga"
        HISTORICAL = "Historical"
        ART = "Art"
        SCIENCE = "Science"
        THRILLER = "Thriller"
