from book import Book        # Given
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
