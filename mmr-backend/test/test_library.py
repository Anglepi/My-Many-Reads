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
    assert_that(library.get_name()).is_equal_to(name)
    assert_that(library.get_owner()).is_equal_to(owner)
