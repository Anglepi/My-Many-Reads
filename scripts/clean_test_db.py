import psycopg2
import psycopg2.extras
from os import environ

connection = psycopg2.connect(host=environ.get("HOST"),
                              database=environ.get("DATABASE"),
                              user=environ.get("USER"),
                              password=environ.get("PASSWORD"),
                              port=environ.get("PORT"))
cur = connection.cursor(
    cursor_factory=psycopg2.extras.RealDictCursor)

cur.execute("delete from libraries where id>3;")
cur.execute("delete from library_entries where id>1;")
cur.execute(
    "delete from user_recommendation_comments where id>2;")
cur.execute("delete from user_recommendations where id>2;")
connection.commit()
