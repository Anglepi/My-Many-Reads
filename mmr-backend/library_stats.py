from library import Library
from book import Book


class LibraryStats:
    def __init__(self, library: Library) -> None:
        entries_read: list[dict] = list(map(Library.Entry.to_dict, filter(
            lambda entry: entry.is_read(), library.get_entries())))

        self.gather_info(entries_read)

    def gather_info(self, entries: list[dict]) -> None:
        score_weight: float = 0.1
        self.__authors: dict[str, float] = {}
        self.__genres: dict[str, float] = {}

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
