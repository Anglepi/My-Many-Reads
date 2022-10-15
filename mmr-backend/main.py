from ctypes.util import find_library
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


@mmr.get("/")
async def root():
    return {"message": "Hello World!"}


@mmr.get("/books")
async def get_books():
    return list(map(lambda book: Book.to_dict(book), book_list))


@mmr.get("/books/{isbn}")
async def get_book(isbn: str):
    return list(filter(lambda book: book.to_dict()["ISBN"] == isbn, book_list))


@mmr.get("/libraries/{user}")
async def get_libraries(user: str):
    libraries_from_user = filter(
        lambda lib: lib.get_owner() == user, libraries)
    return list(map(lambda lib: lib.to_dict(), libraries_from_user))


@mmr.get("/libraries/{user}/{library}")
async def get_library(user: str, library: str):
    library = find_library(user, library)
    return library.to_dict()


@mmr.delete("/libraries/{user}/{library}")
async def delete_library(user: str, library: str):
    library = find_library(user, library)
    if library:
        libraries.remove(library)


@mmr.put("/libraries/{user}/{library}/{new_name}")
async def update_library_name(user: str, library: str, new_name: str):
    library = find_library(user, library)
    library.set_name(new_name)


@mmr.post("/libraries/{user}/{library}")
async def create_library(user: str, library: str):
    libraries.append(Library(user, library, list()))


def find_library(owner: str, name: str) -> Library:
    occurrencies = list(filter(
        lambda lib: lib.get_owner() == owner and lib.get_name() == name, libraries))

    return occurrencies[0] if len(occurrencies) else {}
