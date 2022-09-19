import json
import os
from book import Book
from assertpy import assert_that

current_dir = os.path.dirname(__file__)
sample_data_path = "sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)


def test_create_book_from_dict_and_transform_to_dict():
    with open(data_path) as jsonBooks:
        # Given
        jsonObject = json.load(jsonBooks)
        expectedBook: dict = {
            "ISBN": "ABookId",
            "title": "A book",
            "synopsis": "Some random descriptivie text about the book",
            "author": ["Cervantes"],
            "genres": ["Fantasy", "Action"],
            "publisher": "Nova editorial",
            "publishing_date": "2017-10-28"
        }

        # When
        book: Book = Book.fromDict(jsonObject[0])

        # Then
        assert_that(book.toDict()).is_equal_to(expectedBook)


def test_create_book_from_list_and_transform_to_dict():
    with open(data_path) as jsonBooks:
        # Given
        booksData = json.load(jsonBooks)

        # When
        bookList: list[Book] = Book.fromList(booksData)

        # Then
        assert_that(list(map(Book.toDict, bookList))).is_equal_to(booksData)
