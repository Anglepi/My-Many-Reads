import os
import json
from book import Book
from library import Library
from assertpy import assert_that

current_dir = os.path.dirname(__file__)
sample_data_path = "sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)


def test_create_library():
    # Given
    owner = "Sergio"
    name = "Libros de historia"

    # When
    library = Library(owner, name, [])

    # Then
    assert_that(library.get_owner()).is_equal_to(owner)
    assert_that(library.get_name()).is_equal_to(name)
    assert_that(library.get_entries()).is_equal_to([])


def test_create_library_from_dict():
    # Given
    library_dict = {"owner": "Sergio",
                    "name": "Libros de historia", "entries": []}
    expected_library = '{"owner": "Sergio", "name": "Libros de historia", "entries": []}'

    # When
    library = Library.from_dict(library_dict)

    # Then
    assert_that(json.dumps(library.to_dict())).is_equal_to(expected_library)


def test_create_library_with_entries():
    # Given
    owner = "An owner"
    name = "library name"
    with open(data_path) as json_books:
        books_data = json.load(json_books)
        book_list: list[Book] = Book.from_list(books_data)

    entries = get_sample_entries(book_list[0], book_list[1])
    expected_library = '{"owner": "An owner", "name": "library name", "entries": [{"book": '+json.dumps(book_list[0].to_dict(
    ))+', "score": 7, "status": "PLAN TO READ"}, {"book": '+json.dumps(book_list[1].to_dict())+', "score": 10, "status": "COMPLETED"}]}'

    # When
    library = Library(owner, name, entries)

    # Then
    assert_that(json.dumps(library.to_dict())
                ).is_equal_to(expected_library)


def test_add_entry():
    # Given
    owner = "Sergio"
    name = "Libros de historia"
    library = Library(owner, name, [])
    with open(data_path) as json_books:
        books_data = json.load(json_books)
        book_list: list[Book] = Book.from_list(books_data)
    entry = get_sample_entries(book_list[0], book_list[1])[0]
    expected_library = '{"owner": "Sergio", "name": "Libros de historia", "entries": [{"book": '+json.dumps(
        book_list[0].to_dict())+', "score": 7, "status": "PLAN TO READ"}]}'

    # When
    library.add_entry(entry)

    # Then
    assert_that(json.dumps(library.to_dict())).is_equal_to(expected_library)


def test_remove_entry():
    # Given
    owner = "Sergio"
    name = "Libros de historia"
    with open(data_path) as json_books:
        books_data = json.load(json_books)
        book_list: list[Book] = Book.from_list(books_data)
    library = Library(owner, name, get_sample_entries(
        book_list[0], book_list[1]))
    expected_library = '{"owner": "Sergio", "name": "Libros de historia", "entries": [{"book": '+json.dumps(
        book_list[0].to_dict())+', "score": 7, "status": "PLAN TO READ"}]}'

    # When
    library.remove_entry(book_list[1].ISBN)

    # Then
    assert_that(json.dumps(library.to_dict())).is_equal_to(expected_library)


def test_update_entry():
    # Given
    owner = "Sergio"
    name = "Libros de historia"
    with open(data_path) as json_books:
        books_data = json.load(json_books)
        book_list: list[Book] = Book.from_list(books_data)
    library = Library(
        owner, name, [get_sample_entries(book_list[0], book_list[1])[0]])
    expected_library = '{"owner": "Sergio", "name": "Libros de historia", "entries": [{"book": '+json.dumps(
        book_list[1].to_dict())+', "score": 0, "status": "ON HOLD"}]}'

    # When
    library.update_entry(book_list[0].ISBN, Library.Entry(
        book_list[1], 0, "ON HOLD"))

    # Then
    assert_that(json.dumps(library.to_dict())).is_equal_to(expected_library)


def test_has_book():
    # Given
    owner = "An owner"
    name = "library name"
    with open(data_path) as json_books:
        books_data = json.load(json_books)
        book_list: list[Book] = Book.from_list(books_data)

    entries = get_sample_entries(book_list[0], book_list[1])
    expected_library = '{"owner": "An owner", "name": "library name", "entries": [{"book": '+json.dumps(book_list[0].to_dict(
    ))+', "score": 7, "status": "PLAN TO READ"}, {"book": '+json.dumps(book_list[1].to_dict())+', "score": 10, "status": "COMPLETED"}]}'

    # When
    library = Library(owner, name, entries)
    result = library.has_book(book_list[0])

    # Then
    assert_that(result).is_true()


def get_sample_entries(book1: Book, book2: Book):
    return [Library.Entry(book1, 7, "PLAN TO READ"), Library.Entry(book2, 10, "COMPLETED")]
