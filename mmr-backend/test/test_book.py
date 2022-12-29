import json
import os
from book import Book
from assertpy import assert_that

current_dir = os.path.dirname(__file__)
sample_data_path = "sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)


def test_create_book_from_dict_and_transform_to_dict():
    with open(data_path) as json_books:
        # Given
        json_object = json.load(json_books)
        expected_book: dict = {
            "ISBN": "99921-58-10-7",
            "title": "A book",
            "synopsis": "Some random descriptivie text about the book",
            "authors": ["Cervantes"],
            "genres": ["Fantasy", "Action"],
            "publisher": "Nova editorial",
            "publishing_date": "2017-10-28",
            "edition": "1st Edition"
        }

        # When
        book: Book = Book.from_dict(json_object[0])

        # Then
        assert_that(book.to_dict()).is_equal_to(expected_book)


def test_create_book_from_list_and_transform_to_dict():
    with open(data_path) as json_books:
        # Given
        books_data = json.load(json_books)

        # When
        book_list: list[Book] = Book.from_list(books_data)

        # Then
        assert_that(list(map(Book.to_dict, book_list))).is_equal_to(books_data)
