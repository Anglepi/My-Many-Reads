from library import Library
from book import Book


class LibraryStats:
    def __init__(self, library: Library) -> None:
        self.__library = library

        entries_read: list[dict] = list(map(Library.Entry.to_dict, filter(
            lambda entry: entry.is_read(), library.get_entries())))

        self.gather_info(entries_read)

    def gather_info(self, entries: list[dict]) -> None:
        score_weight: float = 1
        self.__authors: dict[str, float] = {}
        self.__genres: dict[Book.Genre, float] = {}

        for entry in entries:
            score_value: float = score_weight * entry["score"]

            for author in entry["book"]["authors"]:
                if author not in self.__authors:
                    self.__authors[author] = 0
                self.__authors[author] += score_value

            for genre in entry["book"]["genres"]:
                if genre not in self.__genres:
                    self.__genres[genre] = 0
                self.__genres[genre] += score_value

    def score_book(self, book: Book) -> float:
        score: float = 0

        for author in book.authors:
            if author in self.__authors:
                score += self.__authors[author]

        for genre in book.genres:
            if genre in self.__genres:
                score += self.__genres[genre]

        return score

    def get_recommendations(self, books: list[Book]) -> list[tuple[Book, float]]:
        new_books: list[Book] = list(filter(
            lambda book: not self.__library.has_book(book), books))

        scored_books: list[tuple[Book, float]] = list(map(
            lambda book: (book, self.score_book(book)), new_books))

        scored_books = sorted(scored_books, key=lambda x: x[1], reverse=True)

        return scored_books[:10]