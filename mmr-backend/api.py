from typing import Iterable, Optional
from book import Book
from library import Library
from user_recommendation import UserRecommendation
import os
import json
from fastapi import FastAPI, Response, status

# For testing...
current_dir = os.path.dirname(__file__)
sample_data_path = "test/sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)
with open(data_path) as json_books:
    books_data = json.load(json_books)
    mock_book_list: list[Book] = Book.from_list(books_data)

mock_libraries: list[Library] = [Library("user1", "myLibrary", list()), Library(
    "user1", "myOtherLibrary", list()), Library("user2", "generic", [Library.Entry("RandomBook", 5, Library.ReadingStatus.COMPLETED)])]
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
async def get_books() -> list[dict]:
    return list(map(lambda book: Book.to_dict(book), mock_book_list))


@mmr.get("/books/{isbn}")
async def get_book(isbn: str) -> list[dict]:
    matching_book: Iterable = filter(lambda book: book.to_dict()[
        "ISBN"] == isbn, mock_book_list)
    return list(matching_book)

#
# LIBRARIES
#


@mmr.get("/libraries/{user}")
async def get_libraries(user: str) -> list[dict]:
    libraries_from_user = filter(
        lambda lib: lib.get_owner() == user, mock_libraries)
    return list(map(lambda lib: lib.to_dict(), libraries_from_user))


@mmr.get("/libraries/{user}/{library_name}")
async def get_library(user: str, library_name: str) -> dict:
    library: Optional[Library] = find_library(user, library_name)
    return library.to_dict() if library else {}


@mmr.delete("/libraries/{user}/{library_name}")
async def delete_library(user: str, library_name: str) -> None:
    library: Optional[Library] = find_library(user, library_name)
    if library:
        mock_libraries.remove(library)


@mmr.put("/libraries/{user}/{library_name}/{new_name}")
async def update_library_name(user: str, library_name: str, new_name: str) -> None:
    library: Optional[Library] = find_library(user, library_name)
    if library:
        library.set_name(new_name)


@mmr.post("/libraries/{user}/{library_name}")
async def create_library(user: str, library_name: str, response: Response) -> None:
    mock_libraries.append(Library(user, library_name, list()))
    response.status_code = status.HTTP_201_CREATED
    response.headers["location"] = "/libraries/"+user+"/"+library_name


@mmr.post("/libraries/{user}/{library_name}/{isbn}")
async def add_library_entry(user: str, library_name: str, isbn: str, response: Response) -> None:
    library: Optional[Library] = find_library(user, library_name)
    if library:
        library.add_entry(Library.Entry(isbn))
        response.status_code = status.HTTP_201_CREATED


@mmr.delete("/libraries/{user}/{library_name}/{isbn}")
async def remove_library_entry(user: str, library_name: str, isbn: str) -> None:
    library: Optional[Library] = find_library(user, library_name)
    if library:
        library.remove_entry(isbn)


@mmr.put("/libraries/{user}/{library_name}/{isbn}/{score}/{status}")
async def update_library_entry(user: str, library_name: str, isbn: str, score: int, status: Library.ReadingStatus) -> None:
    library: Optional[Library] = find_library(user, library_name)
    if library:
        library.update_entry(isbn, Library.Entry(isbn, score, status))

#
# USER RECOMMENDATIONS
#


@mmr.get("/userRecommendations/{book}")
async def get_recommendations_for_book(book: str) -> list[dict]:
    # More than likely to be replaced with query filter when DB is implemented
    recommendations_for_book = filter(
        lambda recommendation: recommendation.has_book(book), mock_recommendations)

    return list(map(lambda recommendation: recommendation.to_dict(), recommendations_for_book))


def find_library(owner: str, name: str) -> Optional[Library]:
    occurrencies = list(filter(
        lambda lib: lib.get_owner() == owner and lib.get_name() == name, mock_libraries))

    return occurrencies[0] if len(occurrencies) else None
