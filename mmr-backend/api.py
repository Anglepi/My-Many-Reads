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


@mmr.get("/books/{book_id}")
async def get_book(book_id: int, response: Response) -> Union[Optional[Book], dict]:
    book: Optional[Book] = data_manager.get_book(book_id)
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
    success = data_manager.create_library(user, library_name)
    if success:
        response.status_code = status.HTTP_201_CREATED
        response.headers["location"] = "/libraries/"+user+"/"+library_name
    else:
        response.status_code = status.HTTP_409_CONFLICT


@mmr.post("/libraries/{user}/{library_name}/{book_id}")
async def add_library_entry(user: str, library_name: str, book_id: int, response: Response) -> None:
    success: bool = data_manager.add_library_entry(user, library_name, book_id)
    if success:
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_409_CONFLICT


@mmr.delete("/libraries/{user}/{library_name}/{book_id}")
async def remove_library_entry(user: str, library_name: str, book_id: int) -> None:
    data_manager.remove_library_entry(user, library_name, book_id)


@mmr.put("/libraries/{user}/{library_name}/{book_id}/{score}/{status}")
async def update_library_entry(user: str, library_name: str, book_id: int, score: int, status: Library.ReadingStatus) -> None:
    data_manager.update_library_entry(
        user, library_name, book_id, score, status)

#
# USER RECOMMENDATIONS
#


@mmr.get("/recommendations/{book_id}")
async def get_recommendations_for_book(book_id: int) -> list[dict]:
    return data_manager.get_recommendations_for_book(book_id)


@mmr.get("/recommendations/{user}/{library_name}")
async def get_recommendations_for_library(user: str, library_name: str, response: Response) -> Union[list[tuple[Book, float]], dict]:
    library: Optional[Library] = data_manager.get_library(user, library_name)
    books: list[Book] = data_manager.get_books()

    if not library:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Library or user not found"}
    stats: LibraryStats = LibraryStats(library)

    return stats.get_recommendations(books)


@mmr.post("/recommendations/{book_id1}/{book_id2}/{user}")
async def vote_user_recommendation(book_id1: int, book_id2: int, user: str, response: Response) -> Optional[dict]:
    if book_id1 == book_id2:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Recommendations must be from different books"}

    if not data_manager.vote_user_recommendation(book_id1, book_id2, user):
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Recommendation or comment does not exist"}

    response.status_code = status.HTTP_201_CREATED
    response.headers["location"] = "/recommendations/" + str(book_id1)
    return None


@mmr.post("/recommendations/{book_id1}/{book_id2}/{user}/{comment}")
async def add_user_recommendation(book_id1: int, book_id2: int, user: str, comment: str, response: Response) -> Optional[dict]:
    if book_id1 == book_id2:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Can't recommend a book with itself"}

    result: int = data_manager.create_user_recommendation(
        book_id1, book_id2, user, comment)

    if result == 404:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Can't find some of the indicated books"}
    elif result == 409:
        response.status_code = status.HTTP_409_CONFLICT
    else:
        response.status_code = status.HTTP_201_CREATED
        response.headers["location"] = "/recommendations/" + \
            "/".join((str(book_id1), str(book_id2), user))
    return None

#
# STATS
#


@mmr.get("/books/stats/{book_id}")
async def get_book_stats(book_id: int, response: Response) -> Optional[dict]:
    stats: Optional[dict] = data_manager.get_book_stats(book_id)
    if not stats:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Book not found"}
    return stats
