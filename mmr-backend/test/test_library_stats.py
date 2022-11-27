import json
import os
from book import Book
from library import Library
from library_stats import LibraryStats


current_dir = os.path.dirname(__file__)
sample_data_path = "sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)
with open(data_path) as json_books:
    books_data = json.load(json_books)
    book_list: list[Book] = Book.from_list(books_data)


def test_can_create_stats():
    # Given
    library: Library = Library("user", "name", [Library.Entry(book_list[0], 2, Library.ReadingStatus.DROPPED), Library.Entry(
        book_list[1], 10, Library.ReadingStatus.CURRENTLY_READING), Library.Entry(book_list[2], 0, Library.ReadingStatus.PLAN_TO_READ)])

    # When
    stats: LibraryStats = LibraryStats(library)
