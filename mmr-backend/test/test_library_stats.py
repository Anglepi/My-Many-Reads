import json
import os
from book import Book
from library import Library
from library_stats import LibraryStats
from assertpy import assert_that


current_dir = os.path.dirname(__file__)
sample_data_path = "sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)
with open(data_path) as json_books:
    books_data = json.load(json_books)
    book_list: list[Book] = Book.from_list(books_data)


def test_score_book():
    # Given
    library1: Library = Library("user", "name", [Library.Entry(
        book_list[0], 2, Library.ReadingStatus.COMPLETED)])
    stats1: LibraryStats = LibraryStats(library1)
    library2: Library = Library("user", "name", [Library.Entry(book_list[0], 2, Library.ReadingStatus.DROPPED), Library.Entry(
        book_list[1], 10, Library.ReadingStatus.CURRENTLY_READING), Library.Entry(book_list[2], 0, Library.ReadingStatus.PLAN_TO_READ)])
    stats2: LibraryStats = LibraryStats(library2)

    # When
    score1 = stats1.score_book(book_list[2])
    score2 = stats2.score_book(book_list[2])

    # Then
    assert_that(score1).is_equal_to(6)
    assert_that(score2).is_close_to(24.5, 0.25)


def test_recommendations():
    # Given
    library: Library = Library("user", "name", [Library.Entry(
        book_list[2], 7, Library.ReadingStatus.COMPLETED)])
    stats: LibraryStats = LibraryStats(library)
    expected_recommendations = [
        (book_list[0], 21), (book_list[1], 21), (book_list[3], 7), (book_list[4], 0)]

    # When
    recommendations = stats.get_recommendations(book_list)

    # Then
    assert_that(recommendations).is_equal_to(expected_recommendations)
