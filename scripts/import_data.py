# This script is aimed to import a specific dataset with specific structure.
# The dataset will not be uploaded to the repository, since it is available
# here: https://zenodo.org/record/4265096

# This script will NOT check for existing books, authors or genres in the database


import psycopg2
import psycopg2.extras
import os
import csv
import re
from datetime import datetime

connection = psycopg2.connect(host=os.environ.get("HOST"),
                              database=os.environ.get("DATABASE"),
                              user=os.environ.get("USER"),
                              password=os.environ.get("PASSWORD"),
                              port=os.environ.get("PORT"))
cur = connection.cursor(
    cursor_factory=psycopg2.extras.RealDictCursor)

current_dir = os.path.dirname(__file__)
sample_data_path = "books_1.Best_Books_Ever.csv"
data_path = os.path.join(current_dir, sample_data_path)

added_authors: dict = {}
added_genres: dict = {}

default_Ymd_date = '1984-01-1'
default_dmy_date = '01/01/84'


def escape_string(string: str) -> str:
    return string.replace("'", "")


def import_authors(authors: list[str]) -> list[int]:
    ids: list[int] = []
    new_authors: list[str] = []
    for author in authors:
        author = escape_string(author)
        if author in added_authors:
            ids.append(added_authors[author])
        else:
            new_authors.append(author)

    if len(new_authors) > 0:
        query: str = "insert into authors(name, birth_date) values "
        values: list[str] = []
        for author in new_authors:
            # This dataset does not contain author birth date
            values.append("('"+author+"', '"+default_Ymd_date+"')")
        query += ",".join(values) + "returning id, name;"

        cur.execute(query)
        result = cur.fetchall()
        for tuple in result:
            added_authors[tuple["name"]] = tuple["id"]
            ids.append(tuple["id"])
    return ids


def import_genres(genres: list[str]) -> list[int]:
    ids: list[int] = []
    new_genres: list[str] = []
    for genre in genres:
        if genre in added_genres:
            ids.append(added_genres[genre])
        else:
            new_genres.append(genre)

    if len(new_genres) > 0:
        query: str = "insert into genres(genre) values "
        values: list[str] = []
        for genre in new_genres:
            values.append("('"+genre+"')")
        query += ",".join(values) + "returning id, genre;"

        cur.execute(query)
        result = cur.fetchall()
        for tuple in result:
            added_genres[tuple["genre"]] = tuple["id"]
            ids.append(tuple["id"])
    return ids


def import_book(isbn: str, title: str, synopsis: str, publisher: str, publishing_date: str, edition: str) -> int:
    query: str = "insert into books(isbn, title, synopsis, publisher, publishing_date, edition) values "
    try:
        publish_date = datetime.strptime(publishing_date, "%m/%d/%y")
    except ValueError:
        publish_date = datetime.strptime(default_dmy_date, "%m/%d/%y")
    formatted_publish_date = datetime.strftime(publish_date, "%Y-%m-%d")
    query += "('"+escape_string(isbn)+"', '"+escape_string(title)+"', '"+escape_string(synopsis)+"', '" + \
        escape_string(publisher)+"', '"+escape_string(formatted_publish_date) + \
        "', '"+escape_string(edition)+"') returning id;"

    cur.execute(query)
    result = cur.fetchone()
    return result["id"]


def set_authored(book_id: int, author_ids: list[int]) -> None:
    query: str = "insert into authored(book_id, author_id) values "
    values: list[str] = []
    for author_id in author_ids:
        values.append("("+str(book_id)+", "+str(author_id)+")")
    query += ",".join(values) + ";"
    cur.execute(query)


def set_book_genres(book_id: int, genres_ids: list[int]) -> None:
    query: str = "insert into book_genres(book_id, genre_id) values "
    values: list[str] = []
    for genre_id in genres_ids:
        values.append("("+str(book_id)+", "+str(genre_id)+")")
    query += ",".join(values) + ";"
    cur.execute(query)


def import_row(row: dict) -> None:
    authors: list[str] = row["author"].split(",")

    author_ids: list[int] = import_authors(authors)

    genres: list[str] = re.sub(
        '['+re.escape("[] '")+']', '', row["genres"]).split(",")

    genres_ids: list[int] = import_genres(genres)

    book_id: int = import_book(row["isbn"], row["title"], row["description"],
                               row["publisher"], row["publishDate"], row["edition"])

    set_authored(book_id, author_ids)

    set_book_genres(book_id, genres_ids)


with open(data_path, mode='r') as csvfile:
    dict_reader = csv.DictReader(csvfile, delimiter=',')
    current_line = 0
    for row in dict_reader:
        if current_line == 0:
            print('Column names are' + ", ".join(row))
        elif current_line < 3000:
            import_row(row)
        else:
            break
        current_line += 1
    connection.commit()
