import os
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
    library = Library(owner, name)

    # Then
    check_library_data(library, owner, name, [])


def test_create_library_with_entries():
    # Given
    owner = "An owner"
    name = "library name"
    entries = get_sample_entries()

    # When
    library = Library(owner, name, entries)

    # Then
    check_library_data(library, owner, name, entries)


def check_library_data(library: Library, expected_owner: str, expected_name: str, expected_entries: list[Library.Entry]):
    assert_that(library.get_name()).is_equal_to(expected_name)
    assert_that(library.get_owner()).is_equal_to(expected_owner)
    assert_that(library.get_entries()).is_equal_to(expected_entries)


def get_sample_entries():
    return [Library.Entry("first book id", 7, "PLAN TO READ"), Library.Entry("second book id", 10, "COMPLETED")]
