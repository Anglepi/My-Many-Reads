from assertpy import assert_that
from fastapi.testclient import TestClient
from main import mmr
import os
import json
from book import Book
from library import Library


current_dir = os.path.dirname(__file__)
sample_data_path = "sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)
with open(data_path) as json_books:
    books_data = json.load(json_books)
    book_list: list[Book] = Book.from_list(books_data)


def check_response(response, status, body):
    assert_that(response.status_code).is_equal_to(status)
    assert_that(response.json()).is_equal_to(body)


def test_api_initialized():
    with TestClient(mmr) as client:
        response = client.get("/")
    expected_status = 200
    expected_body = {"message": "Hello World!"}

    check_response(response, expected_status, expected_body)


def test_get_books():
    with TestClient(mmr) as client:
        response = client.get("/books")
    expected_status = 200
    expected_body = list(map(lambda book: book.to_dict(), book_list))

    check_response(response, expected_status, expected_body)


def test_get_book():
    with TestClient(mmr) as client:
        response = client.get("/books/ABookId")
    expected_status = 200
    expected_body = [book_list[0].to_dict()]

    check_response(response, expected_status, expected_body)


def test_get_book_not_found():
    with TestClient(mmr) as client:
        response = client.get("/books/IJustMadeThisUp")
    expected_status = 200
    expected_body = []

    check_response(response, expected_status, expected_body)
