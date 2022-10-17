import os
import json
from library import Library
from assertpy import assert_that

current_dir = os.path.dirname(__file__)
sample_data_path = "sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)


def test_create_library():
    # Given
    owner = "Sergio"
    name = "Libros de historia"
    expected_library = '{"owner": "Sergio", "name": "Libros de historia", "entries": []}'

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
    entries = get_sample_entries()
    expected_library = '{"owner": "An owner", "name": "library name", "entries": [{"book_id": "first book id", "score": 7, "status": "PLAN TO READ"}, {"book_id": "second book id", "score": 10, "status": "COMPLETED"}]}'

    # When
    library = Library(owner, name, entries)

    # Then
    assert_that(json.dumps(library.to_dict())).is_equal_to(expected_library)


def test_add_entry():
    # Given
    owner = "Sergio"
    name = "Libros de historia"
    library = Library(owner, name, [])
    entry = get_sample_entries()[0]
    expected_library = '{"owner": "Sergio", "name": "Libros de historia", "entries": [{"book_id": "first book id", "score": 7, "status": "PLAN TO READ"}]}'

    # When
    library.add_entry(entry)

    # Then
    assert_that(json.dumps(library.to_dict())).is_equal_to(expected_library)


def test_remove_entry():
    # Given
    owner = "Sergio"
    name = "Libros de historia"
    library = Library(owner, name, get_sample_entries())
    expected_library = '{"owner": "Sergio", "name": "Libros de historia", "entries": [{"book_id": "first book id", "score": 7, "status": "PLAN TO READ"}]}'

    # When
    library.remove_entry("second book id")

    # Then
    assert_that(json.dumps(library.to_dict())).is_equal_to(expected_library)


def test_update_entry():
    # Given
    owner = "Sergio"
    name = "Libros de historia"
    library = Library(owner, name, [get_sample_entries()[0]])
    expected_library = '{"owner": "Sergio", "name": "Libros de historia", "entries": [{"book_id": "some other new book", "score": 0, "status": "ON HOLD"}]}'

    # When
    library.update_entry("first book id", Library.Entry(
        "some other new book", 0, "ON HOLD"))

    # Then
    assert_that(json.dumps(library.to_dict())).is_equal_to(expected_library)


def get_sample_entries():
    return [Library.Entry("first book id", 7, "PLAN TO READ"), Library.Entry("second book id", 10, "COMPLETED")]
