from typing import Optional, Union
from book import Book
from data_manager import DataManager
from library import Library
from library_stats import LibraryStats
from fastapi import FastAPI, Response, status


data_manager: DataManager = DataManager()

mmr = FastAPI()

#
# BOOKS
#


@mmr.get("/books")
async def get_books() -> list[Book]:
    return data_manager.get_books()


@mmr.get("/books/{isbn}")
async def get_book(isbn: str, response: Response) -> Union[Optional[Book], dict]:
    book: Optional[Book] = data_manager.get_book(isbn)
    if not book:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Book not found"}
    return book

#
# LIBRARIES
#


@mmr.get("/libraries/{user}")
async def get_libraries(user: str) -> list[dict]:
    return data_manager.get_libraries_from_user(user)


@mmr.get("/libraries/{user}/{library_name}")
async def get_library(user: str, library_name: str) -> dict:
    library: Optional[Library] = data_manager.get_library(user, library_name)
    return library.to_dict() if library else {}


@mmr.delete("/libraries/{user}/{library_name}")
async def delete_library(user: str, library_name: str) -> None:
    data_manager.delete_library(user, library_name)


@mmr.put("/libraries/{user}/{library_name}/{new_name}")
async def update_library_name(user: str, library_name: str, new_name: str) -> None:
    data_manager.rename_library(user, library_name, new_name)


@mmr.post("/libraries/{user}/{library_name}")
async def create_library(user: str, library_name: str, response: Response) -> None:
    data_manager.create_library(user, library_name)
    response.status_code = status.HTTP_201_CREATED
    response.headers["location"] = "/libraries/"+user+"/"+library_name


@mmr.post("/libraries/{user}/{library_name}/{isbn}")
async def add_library_entry(user: str, library_name: str, isbn: str, response: Response) -> None:
    success: bool = data_manager.add_library_entry(user, library_name, isbn)
    if success:
        response.status_code = status.HTTP_201_CREATED


@mmr.delete("/libraries/{user}/{library_name}/{isbn}")
async def remove_library_entry(user: str, library_name: str, isbn: str) -> None:
    data_manager.remove_library_entry(user, library_name, isbn)


@mmr.put("/libraries/{user}/{library_name}/{isbn}/{score}/{status}")
async def update_library_entry(user: str, library_name: str, isbn: str, score: int, status: Library.ReadingStatus) -> None:
    data_manager.update_library_entry(user, library_name, isbn, score, status)

#
# USER RECOMMENDATIONS
#


@mmr.get("/recommendations/{isbn}")
async def get_recommendations_for_book(isbn: str) -> list[dict]:
    return data_manager.get_recommendations_for_book(isbn)


@mmr.get("/recommendations/{user}/{library_name}")
async def get_recommendations_for_library(user: str, library_name: str, response: Response) -> Union[list[tuple[Book, float]], dict]:
    library: Optional[Library] = data_manager.get_library(user, library_name)
    books: list[Book] = data_manager.get_books()

    if not library:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Library or user not found"}
    stats: LibraryStats = LibraryStats(library)

    return stats.get_recommendations(books)


@mmr.post("/recommendations/{isbn1}/{isbn2}/{user}")
async def vote_user_recommendation(isbn1: str, isbn2: str, user: str, response: Response) -> Optional[dict]:
    if isbn1 == isbn2:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Recommendations must be from different books"}

    if not data_manager.vote_user_recommendation(isbn1, isbn2, user):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Recommendation or comment does not exist"}

    response.status_code = status.HTTP_201_CREATED
    response.headers["location"] = "/recommendations/" + isbn1
    return None


@mmr.post("/recommendations/{isbn1}/{isbn2}/{user}/{comment}")
async def add_user_recommendation(isbn1: str, isbn2: str, user: str, comment: str, response: Response) -> Optional[dict]:
    if isbn1 == isbn2:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Can't recommend a book with itself"}

    if not data_manager.create_user_recommendation(isbn1, isbn2, user, comment):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Can't find some of the indicated books"}

    response.status_code = status.HTTP_201_CREATED
    response.headers["location"] = "/recommendations/" + \
        "/".join((isbn1, isbn2, user))
    return None
