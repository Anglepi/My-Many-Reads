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
            "isbn": "99921-58-10-7",
            "title": "A book",
            "synopsis": "Some random descriptivie text about the book",
            "authors": ["Cervantes"],
            "genres": ["Action", "Fantasy"],
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


def test_validate_isbn_10():
    # Given
    isbn_10 = "0-545-01022-5"

    # When
    result = Book.validate_isbn(isbn_10)

    # Then
    assert_that(result).is_true()


def test_validate_isbn_13():
    # Given
    isbn_13 = "978-3-16-148410-0"

    # When
    result = Book.validate_isbn(isbn_13)

    # Then
    assert_that(result).is_true()


def test_validate_isbn_with_x():
    # Given
    isbn_x = "0-9752298-0-X"

    # When
    result = Book.validate_isbn(isbn_x)

    # Then
    assert_that(result).is_true()


def test_invalid_isbn_exception():
    # Given
    invalid_isbn = "0-9722298-0-X"

    # When
    try:
        result = Book.validate_isbn(invalid_isbn)
    except Exception as e:
        # Then
        assert_that(str(e)).is_equal_to("Malformed ISBN")
