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
        def __init__(self, bookId: str, score: int, status: Library.ReadingStatus):
            self.__bookId: str = bookId
            self.__score: int = score
            self.__status: Library.ReadingStatus = status

