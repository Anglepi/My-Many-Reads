from typing import Iterable, Optional, Union
from book import Book
from data_manager import DataManager
from library import Library
from library_stats import LibraryStats
from user_recommendation import UserRecommendation
import os
import json
from fastapi import FastAPI, Response, status

# For testing...
current_dir = os.path.dirname(__file__)
sample_data_path = "test/sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)

data_manager: DataManager = DataManager(data_path)

mock_book_list: list[Book] = data_manager.get_books()
mock_libraries: list[Library] = [Library("user1", "myLibrary", list()), Library(
    "user1", "myOtherLibrary", list()), Library("user2", "generic", [Library.Entry(mock_book_list[0], 5, Library.ReadingStatus.COMPLETED)])]
mock_recommendations: list[UserRecommendation] = [UserRecommendation(
    (mock_book_list[0].ISBN, mock_book_list[1].ISBN), UserRecommendation.UserComment("Recommender", "first book is similar to second book")),
    UserRecommendation(
    (mock_book_list[0].ISBN, mock_book_list[2].ISBN), UserRecommendation.UserComment("Recommender", "first book is similar to third book"))]
mock_recommendations[0].add_comment(
    UserRecommendation.UserComment("RandomGuy", "They are both cool"))


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
    library: Optional[Library] = find_library(user, library_name)
    if library:
        library.remove_entry(isbn)


@mmr.put("/libraries/{user}/{library_name}/{isbn}/{score}/{status}")
async def update_library_entry(user: str, library_name: str, isbn: str, score: int, status: Library.ReadingStatus) -> None:
    library: Optional[Library] = find_library(user, library_name)
    book: Optional[Book] = find_book(isbn)
    if library and book:
        library.update_entry(isbn, Library.Entry(book, score, status))

#
# USER RECOMMENDATIONS
#


@mmr.get("/recommendations/{book}")
async def get_recommendations_for_book(book: str) -> list[dict]:
    # More than likely to be replaced with query filter when DB is implemented
    recommendations_for_book: Iterable[UserRecommendation] = filter(
        lambda recommendation: recommendation.has_book(book), mock_recommendations)

    return list(map(lambda recommendation: recommendation.to_dict(), recommendations_for_book))


@mmr.get("/recommendations/{user}/{library_name}")
async def get_recommendations_for_library(user: str, library_name: str, response: Response) -> Union[list[tuple[Book, float]], dict]:
    library: Optional[Library] = find_library(user, library_name)

    if not library:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Library or user not found"}
    stats: LibraryStats = LibraryStats(library)

    return stats.get_recommendations(mock_book_list)


@mmr.post("/recommendations/{book1}/{book2}/{user}")
async def vote_user_recommendation(book1: str, book2: str, user: str, response: Response) -> Optional[dict]:
    existing_recommendation: list[UserRecommendation] = list(filter(lambda recommendation: recommendation.has_book(
        book1) and recommendation.has_book(book2) and len(recommendation.get_author_comments(user)), mock_recommendations))

    if book1 == book2:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Recommendations must be from different books"}

    if len(existing_recommendation):
        existing_recommendation[0].vote_comment(user)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Recommendation or comment does not exist"}

    response.status_code = status.HTTP_201_CREATED
    response.headers["location"] = "/recommendations/" + book1
    return None


@mmr.post("/recommendations/{book1}/{book2}/{user}/{comment}")
async def add_user_recommendation(book1: str, book2: str, user: str, comment: str, response: Response) -> Optional[dict]:
    existing_recommendation: list[UserRecommendation] = list(filter(lambda recommendation: recommendation.has_book(
        book1) and recommendation.has_book(book2), mock_recommendations))

    if book1 == book2:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Can't recommend a book with itself"}

    existing_books: list[Book] = list(
        filter(lambda book: book.ISBN == book1 or book.ISBN == book2, mock_book_list))
    if len(existing_books) != 2:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Can't find some of the indicated books"}

    if len(existing_recommendation):
        existing_recommendation[0].add_comment(
            UserRecommendation.UserComment(user, comment))
    else:
        mock_recommendations.append(UserRecommendation(
            (book1, book2), UserRecommendation.UserComment(user, comment)))

    response.status_code = status.HTTP_201_CREATED
    response.headers["location"] = "/recommendations/" + \
        "/".join((book1, book2, user))
    return None


def find_library(owner: str, name: str) -> Optional[Library]:
    occurrencies = list(filter(
        lambda lib: lib.get_owner() == owner and lib.get_name() == name, mock_libraries))

    return occurrencies[0] if len(occurrencies) else None


def find_book(isbn: str) -> Optional[Book]:
    occurrencies = list(filter(lambda book: book.to_dict()[
        "ISBN"] == isbn, mock_book_list))
    return occurrencies[0] if len(occurrencies) else None
