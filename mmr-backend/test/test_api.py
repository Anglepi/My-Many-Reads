from assertpy import assert_that
from fastapi.testclient import TestClient
from api import mmr
import os
import json
import copy
from book import Book
from library import Library


current_dir = os.path.dirname(__file__)
sample_data_path = "sample-data/books.json"
data_path = os.path.join(current_dir, sample_data_path)
with open(data_path) as json_books:
    books_data = json.load(json_books)
    book_list: list[Book] = Book.from_list(books_data)


def check_response(response, status, body):
    assert_that(response.status_code).is_equal_to(status)
    assert_that(response.json()).is_equal_to(body)


def test_get_books():
    with TestClient(mmr) as client:
        response = client.get("/books")
    expected_status = 200
    expected_body = list(map(lambda book: book.to_dict(), book_list))

    check_response(response, expected_status, expected_body)


def test_get_book():
    with TestClient(mmr) as client:
        response = client.get("/books/ABookId")
    expected_status = 200
    expected_body = [book_list[0].to_dict()]

    check_response(response, expected_status, expected_body)


def test_get_book_not_found():
    with TestClient(mmr) as client:
        response = client.get("/books/IJustMadeThisUp")
    expected_status = 200
    expected_body = []

    check_response(response, expected_status, expected_body)


def test_get_libraries():
    with TestClient(mmr) as client:
        response = client.get("/libraries/user1")
    expected_status = 200
    expected_body = [{"owner": "user1", "name": "myLibrary", "entries": []}, {
        "owner": "user1", "name": "myOtherLibrary", "entries": []}]

    check_response(response, expected_status, expected_body)


def test_get_library():
    with TestClient(mmr) as client:
        response = client.get("/libraries/user2/generic")
    expected_status = 200
    expected_body = {"owner": "user2", "name": "generic", "entries": [
        {"book_id": "RandomBook", "score": 5, "status": "COMPLETED"}]}

    check_response(response, expected_status, expected_body)


def test_create_library():
    with TestClient(mmr) as client:
        libraries = client.get("/libraries/userTest").json()
        response = client.post("/libraries/userTest/libraryTest")
        new_libraries = client.get("/libraries/userTest").json()

    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers["location"]).is_equal_to(
        "/libraries/userTest/libraryTest")
    assert_that(libraries).is_not_equal_to(new_libraries)
    assert_that(new_libraries).is_equal_to(
        [{"owner": "userTest", "name": "libraryTest", "entries": []}])


def test_update_library():
    with TestClient(mmr) as client:
        libraries = client.get("/libraries/userTest").json()
        response = client.put("/libraries/userTest/libraryTest/newNameTest")
        new_libraries = client.get("/libraries/userTest").json()

    assert_that(response.status_code).is_equal_to(200)
    assert_that(libraries).is_not_equal_to(new_libraries)
    assert_that(new_libraries).is_equal_to(
        [{"owner": "userTest", "name": "newNameTest", "entries": []}])


def test_delete_nonexistent_library():
    with TestClient(mmr) as client:
        libraries = client.get("/libraries/userTest").json()
        response = client.delete("/libraries/userTest/libraryTest")
        new_libraries = client.get("/libraries/userTest").json()

    assert_that(response.status_code).is_equal_to(200)
    assert_that(libraries).is_equal_to(new_libraries)


def test_delete_library():
    with TestClient(mmr) as client:
        libraries = client.get("/libraries/userTest").json()
        response = client.delete("/libraries/userTest/newNameTest")
        new_libraries = client.get("/libraries/userTest").json()

    assert_that(response.status_code).is_equal_to(200)
    assert_that(libraries).is_not_equal_to(new_libraries)
    assert_that(new_libraries).is_equal_to([])


def test_library_add_entry():
    with TestClient(mmr) as client:
        library = client.get("/libraries/user1/myLibrary").json()
        response = client.post("/libraries/user1/myLibrary/testBook")
        updated_library = client.get("/libraries/user1/myLibrary").json()

    assert_that(response.status_code).is_equal_to(201)
    assert_that(library).is_not_equal_to(updated_library)
    assert_that(updated_library["entries"]).is_equal_to(
        [{"book_id": "testBook", "score": None, "status": None}])


def test_library_update_entry():
    with TestClient(mmr) as client:
        library = client.get("/libraries/user1/myLibrary").json()
        response = client.put(
            "/libraries/user1/myLibrary/testBook/10/COMPLETED")
        updated_library = client.get("/libraries/user1/myLibrary").json()

    assert_that(response.status_code).is_equal_to(200)
    assert_that(library).is_not_equal_to(updated_library)
    assert_that(updated_library["entries"]).is_equal_to(
        [{"book_id": "testBook", "score": 10, "status": "COMPLETED"}])


def test_remove_nonexistent_entry():
    with TestClient(mmr) as client:
        library = client.get("/libraries/user1/myLibrary").json()
        response = client.delete(
            "/libraries/user1/myLibrary/nonexistent")
        updated_library = client.get("/libraries/user1/myLibrary").json()

    assert_that(response.status_code).is_equal_to(200)
    assert_that(library).is_equal_to(updated_library)


def test_remove_existent_entry():
    with TestClient(mmr) as client:
        library = client.get("/libraries/user1/myLibrary").json()
        response = client.delete(
            "/libraries/user1/myLibrary/testBook")
        updated_library = client.get("/libraries/user1/myLibrary").json()

    assert_that(response.status_code).is_equal_to(200)
    assert_that(library).is_not_equal_to(updated_library)
    assert_that(updated_library["entries"]).is_equal_to([])


def test_user_recommendations_for_book():
    with TestClient(mmr) as client:
        recommendations1 = client.get(
            "/recommendations/ThirdBookId")
        recommendations2 = client.get(
            "/recommendations/NotExistent")
    expected_status = 200
    expected_body1 = [
        {
            "books": [
                "ABookId",
                "ThirdBookId"
            ],
            "comments": [
                {
                    "author": "Recommender",
                    "comment": "first book is similar to third book",
                    "score": 0
                }
            ]
        }
    ]
    expected_body2 = []

    check_response(recommendations1, expected_status, expected_body1)
    check_response(recommendations2, expected_status, expected_body2)


def test_add_user_recommendation_duplicated_books():
    with TestClient(mmr) as client:
        response = client.post(
            "/recommendations/ABookId/ABookId/username/comment")

    check_response(response, 400, {
                   "error": "Can't recommend a book with itself"})


def test_add_user_recommendation_missing_book():
    with TestClient(mmr) as client:
        response = client.post(
            "/recommendations/ABookId/NonExistentBook/username/comment")

    check_response(response, 404, {
                   "error": "Can't find some of the indicated books"})


def test_vote_user_recommendation():
    with TestClient(mmr) as client:
        existing_recommendations = client.get(
            "/recommendations/ABookId").json()
        response = client.post(
            "/recommendations/ABookId/SecondBookId/Recommender")
        new_recommendations = client.get(
            "/recommendations/ABookId").json()

    previous_score = existing_recommendations[0]["comments"][0]["score"]
    new_score = new_recommendations[0]["comments"][0]["score"]

    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers["location"]).is_equal_to(
        "/recommendations/ABookId")
    assert_that(new_score).is_equal_to(previous_score+1)


def test_vote_user_bad_recommendation():
    with TestClient(mmr) as client:
        response = client.post(
            "/recommendations/ABookId/ABookId/Recommender")

    check_response(response, 400, {
                   "error": "Recommendations must be from different books"})


def test_vote_user_recommendation_missing_author():
    with TestClient(mmr) as client:
        response = client.post(
            "/recommendations/ABookId/SecondBookId/ThisUserHasNotCommentedHere")

    check_response(response, 404, {
                   "error": "Recommendation or comment does not exist"})


def test_add_user_recommendation_new():
    with TestClient(mmr) as client:
        existing_recommendations = client.get(
            "/recommendations/SecondBookId").json()
        response = client.post(
            "/recommendations/SecondBookId/ThirdBookId/username/comment")
        new_recommendations = client.get(
            "/recommendations/SecondBookId").json()
    expected_new_recommendations = copy.deepcopy(existing_recommendations)
    expected_new_recommendations.append(
        {"books": ["SecondBookId", "ThirdBookId"], "comments": [{"author": "username", "comment": "comment", "score": 0}]})

    assert_that(existing_recommendations).is_not_equal_to(new_recommendations)
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers["location"]).is_equal_to(
        "/recommendations/SecondBookId/ThirdBookId/username")
    assert_that(new_recommendations).is_equal_to(expected_new_recommendations)


def test_add_user_recommendation_existing():
    with TestClient(mmr) as client:
        existing_recommendations = client.get(
            "/recommendations/ABookId").json()
        response = client.post(
            "/recommendations/ABookId/ThirdBookId/username/comment")
        new_recommendations = client.get(
            "/recommendations/ABookId").json()
    expected_new_recommendations = copy.deepcopy(existing_recommendations)
    expected_new_recommendations[1]["comments"].append(
        {"author": "username", "comment": "comment", "score": 0})

    assert_that(existing_recommendations).is_not_equal_to(new_recommendations)
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers["location"]).is_equal_to(
        "/recommendations/ABookId/ThirdBookId/username")
    assert_that(new_recommendations).is_equal_to(expected_new_recommendations)
