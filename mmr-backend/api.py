from typing import Iterable, Optional
from book import Book
from library import Library
import os
import json
from fastapi import FastAPI

# For testing...
current_dir = os.path.dirname(__file__)
sample_data_path = "test/sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)
with open(data_path) as json_books:
    books_data = json.load(json_books)
    book_list: list[Book] = Book.from_list(books_data)

libraries: list[Library] = [Library("user1", "myLibrary", list()), Library(
    "user1", "myOtherLibrary", list()), Library("user2", "generic", [Library.Entry("RandomBook", 5, Library.ReadingStatus.COMPLETED)])]


mmr = FastAPI()


@mmr.get("/books")
async def get_books() -> list[dict]:
    return list(map(lambda book: Book.to_dict(book), book_list))


@mmr.get("/books/{isbn}")
async def get_book(isbn: str) -> list[dict]:
    matching_book: Iterable = filter(lambda book: book.to_dict()[
        "ISBN"] == isbn, book_list)
    return list(matching_book)


@mmr.get("/libraries/{user}")
async def get_libraries(user: str) -> list[dict]:
    libraries_from_user = filter(
        lambda lib: lib.get_owner() == user, libraries)
    return list(map(lambda lib: lib.to_dict(), libraries_from_user))


@mmr.get("/libraries/{user}/{library_name}")
async def get_library(user: str, library_name: str) -> dict:
    library: Optional[Library] = find_library(user, library_name)
    return library.to_dict() if library else {}


@mmr.delete("/libraries/{user}/{library_name}")
async def delete_library(user: str, library_name: str) -> None:
    library: Optional[Library] = find_library(user, library_name)
    if library:
        libraries.remove(library)


@mmr.put("/libraries/{user}/{library_name}/{new_name}")
async def update_library_name(user: str, library_name: str, new_name: str) -> None:
    library: Optional[Library] = find_library(user, library_name)
    if library:
        library.set_name(new_name)


@mmr.post("/libraries/{user}/{library_name}")
async def create_library(user: str, library_name: str) -> None:
    libraries.append(Library(user, library_name, list()))


@mmr.post("/libraries/{user}/{library_name}/{isbn}")
async def add_library_entry(user: str, library_name: str, isbn: str) -> None:
    library: Optional[Library] = find_library(user, library_name)
    if library:
        library.add_entry(Library.Entry(isbn))


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


def find_library(owner: str, name: str) -> Optional[Library]:
    occurrencies = list(filter(
        lambda lib: lib.get_owner() == owner and lib.get_name() == name, libraries))

    return occurrencies[0] if len(occurrencies) else None
