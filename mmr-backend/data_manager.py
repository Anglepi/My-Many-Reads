from __future__ import annotations
from book import Book
from library import Library
from user_recommendation import UserRecommendation
from typing import Optional
import psycopg2
import psycopg2.extras
from os import environ


class DataManager:
    AGGREGATED_VALUE_SEPARATOR = ';'

    def __init__(self) -> None:
        self._connection = psycopg2.connect(host=environ.get("HOST"),
                                            database=environ.get("DATABASE"),
                                            user=environ.get("USER"),
                                            password=environ.get("PASSWORD"),
                                            port=environ.get("PORT"))
        self._cur = self._connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)

    # BOOKS

    def get_books(self) -> list[Book]:
        self._cur.execute(
            "SELECT b.id, b.isbn, b.title, b.synopsis, b.publisher, b.publishing_date, b.edition, " +
            "STRING_AGG(DISTINCT(a.name), %s) as authors, STRING_AGG(DISTINCT(g.genre), %s) " +
            "as genres FROM books b " +
            "left join authored ad on b.id = ad.book_id " +
            "left join authors a on ad.author_id = a.id " +
            "left join book_genres bg on b.id = bg.book_id " +
            "left join genres g on g.id = bg.genre_id " +
            "group by b.id " +
            "order by b.title", (DataManager.AGGREGATED_VALUE_SEPARATOR, DataManager.AGGREGATED_VALUE_SEPARATOR))
        result = self._cur.fetchall()
        for tuple in result:
            tuple["authors"] = tuple["authors"].split(
                DataManager.AGGREGATED_VALUE_SEPARATOR)
            tuple["genres"] = tuple["genres"].split(
                DataManager.AGGREGATED_VALUE_SEPARATOR)
        return Book.from_list(result)

    def get_book(self, book_id: int) -> Optional[Book]:
        self._cur.execute(
            "with found_book as ( " +
            "SELECT b.id, b.isbn, b.title, b.synopsis, b.publisher, b.publishing_date, b.edition, " +
            "STRING_AGG(DISTINCT(a.name), %s) as authors, STRING_AGG(DISTINCT(g.genre), %s) " +
            "as genres FROM books b " +
            "left join authored ad on b.id = ad.book_id " +
            "left join authors a on ad.author_id = a.id " +
            "left join book_genres bg on b.id = bg.book_id " +
            "left join genres g on g.id = bg.genre_id " +
            "where b.id = %s " +
            "group by b.id " +
            ") " +
            "update books b set views = b.views + 1 " +
            "from found_book " +
            "where b.id = found_book.id " +
            "returning found_book.*", (DataManager.AGGREGATED_VALUE_SEPARATOR, DataManager.AGGREGATED_VALUE_SEPARATOR, book_id))
        result = self._cur.fetchone()
        if not result:
            return None
        self._connection.commit()
        result["authors"] = result["authors"].split(
            DataManager.AGGREGATED_VALUE_SEPARATOR)
        result["genres"] = result["genres"].split(
            DataManager.AGGREGATED_VALUE_SEPARATOR)
        return result

    # LIBRARIES

    def get_libraries_from_user(self, user: str) -> list[dict]:
        self._cur.execute(
            "SELECT l.id, l.owner, l.name, le.score, le.reading_status, " +
            "b.id as book_id, b.isbn, b.title, b.synopsis, b.publisher, b.publishing_date, b.edition, " +
            "STRING_AGG(DISTINCT(a.name), %s) as authors, STRING_AGG(DISTINCT(g.genre), %s) as genres " +
            "from libraries l " +
            "left join library_entries le on l.id = le.library_id " +
            "left join books b on b.id = le.book_id " +
            "left join authored ad on b.id = ad.book_id  " +
            "left join authors a on ad.author_id = a.id  " +
            "left join book_genres bg on b.id = bg.book_id  " +
            "left join genres g on g.id = bg.genre_id  " +
            "where l.owner = %s " +
            "group by l.id, le.id, b.id " +
            "order by l.id;", (DataManager.AGGREGATED_VALUE_SEPARATOR, DataManager.AGGREGATED_VALUE_SEPARATOR, user))
        result = self._cur.fetchall()
        libraries: dict[int, Library] = {}
        for tuple in result:
            if tuple["id"] not in libraries.keys():
                libraries[tuple["id"]] = Library(
                    tuple["owner"], tuple["name"], [])
            if tuple["book_id"]:
                tuple["authors"] = tuple["authors"].split(";")
                tuple["genres"] = tuple["genres"].split(";")
                libraries[tuple["id"]].add_entry(Library.Entry(Book(tuple["book_id"], tuple["isbn"], tuple["title"], tuple["synopsis"], tuple["authors"],
                                                 tuple["genres"], tuple["publisher"], tuple["publishing_date"], tuple["edition"]), tuple["score"], tuple["reading_status"]))

        return list(map(lambda lib: lib.to_dict(), libraries.values())) if libraries else []

    def get_library(self, user: str, library_name: str) -> Optional[Library]:
        self._cur.execute(
            "SELECT l.id, l.owner, l.name, le.score, le.reading_status, " +
            "b.id as book_id, b.isbn, b.title, b.synopsis, b.publisher, b.publishing_date, b.edition, " +
            "STRING_AGG(DISTINCT(a.name), %s) as authors, STRING_AGG(DISTINCT(g.genre), %s) as genres " +
            "from libraries l " +
            "left join library_entries le on l.id = le.library_id " +
            "left join books b on b.id = le.book_id " +
            "left join authored ad on b.id = ad.book_id  " +
            "left join authors a on ad.author_id = a.id  " +
            "left join book_genres bg on b.id = bg.book_id  " +
            "left join genres g on g.id = bg.genre_id  " +
            "where l.owner = %s and l.name = %s " +
            "group by l.id, le.id, b.id " +
            "order by l.id;", (DataManager.AGGREGATED_VALUE_SEPARATOR, DataManager.AGGREGATED_VALUE_SEPARATOR, user, library_name))
        result = self._cur.fetchall()
        if not result:
            return None

        library: Library = Library(result[0]["owner"], result[0]["name"], [])
        for tuple in result:
            if tuple["book_id"]:
                tuple["authors"] = tuple["authors"].split(";")
                tuple["genres"] = tuple["genres"].split(";")
                library.add_entry(Library.Entry(Book(tuple["book_id"], tuple["isbn"], tuple["title"], tuple["synopsis"], tuple["authors"],
                                                     tuple["genres"], tuple["publisher"], tuple["publishing_date"], tuple["edition"]), tuple["score"], tuple["reading_status"]))

        return library

    def delete_library(self, user: str, library_name: str) -> None:
        self._cur.execute(
            "update libraries set owner = '', active = false where owner = %s and name = %s", (user, library_name))
        self._connection.commit()

    def rename_library(self, user: str, library_name: str, new_name: str) -> None:
        self._cur.execute(
            "update libraries set name = %s where owner = %s and name = %s", (new_name, user, library_name))
        self._connection.commit()

    def create_library(self, user: str, library_name: str) -> bool:
        try:
            self._cur.execute(
                "insert into libraries (owner, name) values (%s, %s)", (user, library_name))
        except psycopg2.IntegrityError:
            self._connection.rollback()
            return False
        else:
            self._connection.commit()

        return True

    def remove_library_entry(self, user: str, library_name: str, book_id: int) -> None:
        self._cur.execute("delete from library_entries le using libraries l, books b " +
                          "where le.library_id = l.id and b.id = le.book_id and " +
                          "b.id = %s and l.owner = %s and l.name = %s", (book_id, user, library_name))
        self._connection.commit()

    def add_library_entry(self, user: str, library_name: str, book_id: int) -> bool:
        try:
            self._cur.execute("insert into library_entries(library_id, book_id) " +
                              "select l.id, b.id from libraries l, books b " +
                              "where l.owner = %s AND l.name = %s AND b.id = %s", (user, library_name, book_id))
        except psycopg2.IntegrityError:
            self._connection.rollback()
            return False
        else:
            self._connection.commit()
        return True

    def update_library_entry(self, user: str, library_name: str, book_id: int, score: int, status: Library.ReadingStatus) -> None:
        self._cur.execute("update library_entries le set book_id = b.id, score=%s, reading_status=%s " +
                          "from books b, libraries l " +
                          "where l.owner = %s AND l.name = %s AND b.id = %s " +
                          "AND le.library_id = l.id AND le.book_id = b.id", (score, status.value, user, library_name, book_id))
        self._connection.commit()

    # RECOMMENDATIONS

    def get_recommendations_for_book(self, book_id: int) -> list[dict]:
        self._cur.execute("select ur.id, b1.id as book_id1, b2.id as book_id2, urc.author, urc.comment, urc.score " +
                          "from user_recommendations ur " +
                          "left join books b1 on ur.book1_id = b1.id " +
                          "left join books b2 on ur.book2_id = b2.id " +
                          "left join user_recommendation_comments urc on ur.id = urc.recommendation_id " +
                          "where b1.id = %s or b2.id = %s " +
                          "order by urc.score desc, urc.author asc, urc.comment asc", (book_id, book_id))

        result = self._cur.fetchall()
        recommendations: dict[int, UserRecommendation] = {}
        for tuple in result:
            if tuple["id"] not in recommendations.keys():
                recommendations[tuple["id"]] = UserRecommendation(
                    (tuple["book_id1"], tuple["book_id2"]),
                    UserRecommendation.UserComment(
                        tuple["author"], tuple["comment"], tuple["score"])
                )
            else:
                recommendations[tuple["id"]].add_comment(UserRecommendation.UserComment(
                    tuple["author"], tuple["comment"], tuple["score"]))

        return list(map(lambda recommendation: recommendation.to_dict(), recommendations.values()))

    def __getOrCreateRecommendationsPair(self, book_id1: int, book_id2: int) -> Optional[int]:
        self._cur.execute("select ur.id from user_recommendations ur " +
                          "left join books b1 on b1.id = ur.book1_id " +
                          "left join books b2 on b2.id = ur.book2_id " +
                          "where " +
                          "(b1.id = %s and b2.id = %s) " +
                          "or  " +
                          "(b2.id = %s and b1.id = %s)", (book_id1, book_id2, book_id1, book_id2))
        result = self._cur.fetchone()

        if not result:
            self._cur.execute("insert into user_recommendations (book1_id, book2_id) " +
                              "select b1.id as book1_id, b2.id as book2_id from books b1 " +
                              "join books b2 on b1.id = %s and b2.id=%s " +
                              "returning id", (book_id1, book_id2))
            result = self._cur.fetchone()

        return result["id"] if result else None

    def create_user_recommendation(self, book_id1: int, book_id2: int, user: str, comment: str) -> int:
        recommendationPairId: Optional[int] = self.__getOrCreateRecommendationsPair(
            book_id1, book_id2)

        if not recommendationPairId:
            return 404

        try:
            self._cur.execute("insert into user_recommendation_comments (recommendation_id, author, comment) " +
                              "values " +
                              "(%s, %s, %s) " +
                              "returning id", (recommendationPairId, user, comment))
        except psycopg2.IntegrityError:
            self._connection.rollback()
            return 409
        else:
            self._connection.commit()
        result = self._cur.fetchone()
        return 201 if result else 404

    def vote_user_recommendation(self, book_id1: int, book_id2: int, user: str) -> bool:
        self._cur.execute("update user_recommendation_comments urc " +
                          "set score = score + 1 " +
                          "from books b1 " +
                          "join books b2 on b1.id = %s and b2.id= %s " +
                          "join user_recommendations ur " +
                          "on (ur.book1_id = b1.id and ur.book2_id = b2.id) or (ur.book1_id = b2.id and ur.book2_id = b1.id) " +
                          "where ur.id = urc.recommendation_id and urc.author = %s " +
                          "returning urc.id", (book_id1, book_id2, user))
        self._connection.commit()
        result = self._cur.fetchone()
        return True if result else False

    def get_book_stats(self, book_id: int) -> dict:
        self._cur.execute("select b.title, b.views, AVG(le.score) as score, count(distinct l.owner) as readers " +
                          "from books b " +
                          "left join library_entries le on b.id = le.book_id " +
                          "left join libraries l on l.id = le.library_id " +
                          "where b.id = %s " +
                          "group by b.id ", (book_id,))
        return self._cur.fetchone()

    def get_genres_stats(self) -> dict:
        self._cur.execute("select g.genre, sum(b.views) as views, coalesce(AVG(le.score),0) as score, count(distinct l.owner) as readers " +
                          "from books b " +
                          "left join library_entries le on b.id = le.book_id " +
                          "left join libraries l on l.id = le.library_id " +
                          "left join book_genres bg on bg.book_id = b.id " +
                          "left join genres g on g.id = bg.genre_id " +
                          "group by g.genre " +
                          "order by views desc")
        return self._cur.fetchall()
