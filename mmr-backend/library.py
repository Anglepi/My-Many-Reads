from __future__ import annotations
from enum import Enum

class Library:
    def __init__(self, owner, name: str, entries: list[Library.Entry] = []):
        self.__owner = owner
        self.__name: str = name
        self.__entries: list[Library.Entry] = entries

    class ReadingStatus(Enum):
        PLAN_TO_READ = "PLAN TO READ"
        CURRENTLY_READING = "CURRENTLY READING"
        COMPLETED = "COMPLETED"
        DROPPED = "DROPPED"
        ON_HOLD = "ON HOLD"
    
    class Entry:
        def __init__(self, book_id: str, score: int, status: Library.ReadingStatus):
            self.__book_id: str = book_id
            self.__score: int = score
            self.__status: Library.ReadingStatus = status

        def get_book_id(self):
            return self.__book_id

    def add_entry(self, entry: Library.Entry):
        self.__entries.append(entry)

    def update_entry(self, book_id: str, new_entry: Library.Entry):
        for entry in self.__entries:
            if(entry.get_book_id() == book_id):
                entry = new_entry
                break

    def remove_entry(self, book_id: str):
        for entry in self.__entries:
            if(entry.get_book_id() == book_id):
                self.__entries.remove(entry)

    def get_entries(self):
        return self.__entries
