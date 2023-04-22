from os import environ
if environ.get("TEST"):
    import sys
    sys.modules["data_manager"] = __import__("mock_data_manager")
from api import mmr
from book import Book
import copy
import json
import os
from assertpy import assert_that
from fastapi.testclient import TestClient


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
    # Given
    expected_status = 200
    expected_body = list(map(lambda book: book.to_dict(), book_list))

    # When
    with TestClient(mmr) as client:
        response = client.get("/books")

    # Then
    check_response(response, expected_status, expected_body)


def test_get_book():
    # Given
    expected_status = 200
    expected_body = book_list[0].to_dict()

    # When
    with TestClient(mmr) as client:
        response = client.get("/books/99921-58-10-7")

    # Then
    check_response(response, expected_status, expected_body)


def test_get_book_not_found():
    # Given
    expected_status = 404
    expected_body = {"error": "Book not found"}

    # When
    with TestClient(mmr) as client:
        response = client.get("/books/93-86954-21-4")

    # Then
    check_response(response, expected_status, expected_body)


def test_get_libraries():
    # Given
    expected_status = 200
    expected_body = [{"owner": "user1", "name": "myLibrary", "entries": []}, {
        "owner": "user1", "name": "myOtherLibrary", "entries": []}]

    # When
    with TestClient(mmr) as client:
        response = client.get("/libraries/user1")

    # Then
    check_response(response, expected_status, expected_body)


def test_get_library():
    # Given
    expected_status = 200
    expected_body = {"owner": "user2", "name": "generic", "entries": [
        {"book": book_list[0].to_dict(), "score": 5, "status": "COMPLETED"}]}

    # When
    with TestClient(mmr) as client:
        response = client.get("/libraries/user2/generic")

    # Then
    check_response(response, expected_status, expected_body)


def test_create_library():
    # Given - When
    with TestClient(mmr) as client:
        libraries = client.get("/libraries/userTest").json()
        response = client.post("/libraries/userTest/libraryTest")
        new_libraries = client.get("/libraries/userTest").json()

    # Then
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers["location"]).is_equal_to(
        "/libraries/userTest/libraryTest")
    assert_that(libraries).is_not_equal_to(new_libraries)
    assert_that(new_libraries).is_equal_to(
        [{"owner": "userTest", "name": "libraryTest", "entries": []}])


def test_update_library():
    # Given - When
    with TestClient(mmr) as client:
        libraries = client.get("/libraries/userTest").json()
        response = client.put("/libraries/userTest/libraryTest/newNameTest")
        new_libraries = client.get("/libraries/userTest").json()

    # Then
    assert_that(response.status_code).is_equal_to(200)
    assert_that(libraries).is_not_equal_to(new_libraries)
    assert_that(new_libraries).is_equal_to(
        [{"owner": "userTest", "name": "newNameTest", "entries": []}])


def test_delete_nonexistent_library():
    # Given - When
    with TestClient(mmr) as client:
        libraries = client.get("/libraries/userTest").json()
        response = client.delete("/libraries/userTest/libraryTest")
        new_libraries = client.get("/libraries/userTest").json()

    # Then
    assert_that(response.status_code).is_equal_to(200)
    assert_that(libraries).is_equal_to(new_libraries)


def test_delete_library():
    # Given - When
    with TestClient(mmr) as client:
        libraries = client.get("/libraries/userTest").json()
        response = client.delete("/libraries/userTest/newNameTest")
        new_libraries = client.get("/libraries/userTest").json()

    # Then
    assert_that(response.status_code).is_equal_to(200)
    assert_that(libraries).is_not_equal_to(new_libraries)
    assert_that(new_libraries).is_equal_to([])


def test_library_add_entry():
    # Given - When
    with TestClient(mmr) as client:
        library = client.get("/libraries/user1/myLibrary").json()
        response = client.post("/libraries/user1/myLibrary/99921-58-10-7")
        updated_library = client.get("/libraries/user1/myLibrary").json()

    # Then
    assert_that(response.status_code).is_equal_to(201)
    assert_that(library).is_not_equal_to(updated_library)
    assert_that(updated_library["entries"]).is_equal_to(
        [{"book": book_list[0].to_dict(), "score": None, "status": ""}])


def test_library_update_entry():
    # Given - When
    with TestClient(mmr) as client:
        library = client.get("/libraries/user1/myLibrary").json()
        response = client.put(
            "/libraries/user1/myLibrary/99921-58-10-7/10/COMPLETED")
        updated_library = client.get("/libraries/user1/myLibrary").json()

    # Then
    assert_that(response.status_code).is_equal_to(200)
    assert_that(library).is_not_equal_to(updated_library)
    assert_that(updated_library["entries"]).is_equal_to(
        [{"book": book_list[0].to_dict(), "score": 10, "status": "COMPLETED"}])


def test_remove_nonexistent_entry():
    # Given - When
    with TestClient(mmr) as client:
        library = client.get("/libraries/user1/myLibrary").json()
        response = client.delete(
            "/libraries/user1/myLibrary/nonexistent")
        updated_library = client.get("/libraries/user1/myLibrary").json()

    # Then
    assert_that(response.status_code).is_equal_to(200)
    assert_that(library).is_equal_to(updated_library)


def test_remove_existent_entry():
    # Given - When
    with TestClient(mmr) as client:
        library = client.get("/libraries/user1/myLibrary").json()
        response = client.delete(
            "/libraries/user1/myLibrary/99921-58-10-7")
        updated_library = client.get("/libraries/user1/myLibrary").json()

    # Then
    assert_that(response.status_code).is_equal_to(200)
    assert_that(library).is_not_equal_to(updated_library)
    assert_that(updated_library["entries"]).is_equal_to([])


def test_user_recommendations_for_book():
    # Given
    expected_status = 200
    expected_body1 = [
        {
            "books": [
                "0-9752298-0-X",
                "99921-58-10-7"
            ],
            "comments": [
                {
                    "author": "OtherGuy",
                    "comment": "They are both entertaining",
                    "score": 0
                }
            ]
        }
    ]
    expected_body2 = []

    # When
    with TestClient(mmr) as client:
        recommendations1 = client.get(
            "/recommendations/0-9752298-0-X")
        recommendations2 = client.get(
            "/recommendations/NotExistent")

    # Then
    check_response(recommendations1, expected_status, expected_body1)
    check_response(recommendations2, expected_status, expected_body2)


def test_add_user_recommendation_duplicated_books():
    # Given - When
    with TestClient(mmr) as client:
        response = client.post(
            "/recommendations/99921-58-10-7/99921-58-10-7/username/comment")

    # Then
    check_response(response, 400, {
                   "error": "Can't recommend a book with itself"})


def test_add_user_recommendation_missing_book():
    # Given - When
    with TestClient(mmr) as client:
        response = client.post(
            "/recommendations/99921-58-10-7/NonExistentBook/username/comment")

    # Then
    check_response(response, 404, {
                   "error": "Can't find some of the indicated books"})


def test_vote_user_recommendation():
    # Given - When
    with TestClient(mmr) as client:
        existing_recommendations = client.get(
            "/recommendations/9971-5-0210-0").json()
        response = client.post(
            "/recommendations/99921-58-10-7/9971-5-0210-0/RandomGuy")
        new_recommendations = client.get(
            "/recommendations/9971-5-0210-0").json()
    previous_score = existing_recommendations[0]["comments"][0]["score"]
    new_score = new_recommendations[0]["comments"][0]["score"]

    # Then
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers["location"]).is_equal_to(
        "/recommendations/99921-58-10-7")
    assert_that(new_score).is_equal_to(previous_score+1)


def test_vote_user_bad_recommendation():
    # Given - When
    with TestClient(mmr) as client:
        response = client.post(
            "/recommendations/99921-58-10-7/99921-58-10-7/Recommender")

    # Then
    check_response(response, 400, {
                   "error": "Recommendations must be from different books"})


def test_vote_user_recommendation_missing_author():
    # Given - When
    with TestClient(mmr) as client:
        response = client.post(
            "/recommendations/99921-58-10-7/9971-5-0210-0/ThisUserHasNotCommentedHere")

    # Then
    check_response(response, 404, {
                   "error": "Recommendation or comment does not exist"})


def test_add_user_recommendation_new():
    # Given - When
    with TestClient(mmr) as client:
        existing_recommendations = client.get(
            "/recommendations/9971-5-0210-0").json()
        response = client.post(
            "/recommendations/9971-5-0210-0/0-9752298-0-X/username/comment")
        new_recommendations = client.get(
            "/recommendations/9971-5-0210-0").json()
    expected_new_recommendations = copy.deepcopy(existing_recommendations)
    expected_new_recommendations.append(
        {"books": ["0-9752298-0-X", "9971-5-0210-0"], "comments": [{"author": "username", "comment": "comment", "score": 0}]})

    # Then
    assert_that(existing_recommendations).is_not_equal_to(new_recommendations)
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers["location"]).is_equal_to(
        "/recommendations/9971-5-0210-0/0-9752298-0-X/username")
    assert_that(new_recommendations).is_equal_to(expected_new_recommendations)


def test_add_user_recommendation_existing():
    # Given - When
    with TestClient(mmr) as client:
        existing_recommendations = client.get(
            "/recommendations/99921-58-10-7").json()
        response = client.post(
            "/recommendations/99921-58-10-7/0-9752298-0-X/username/comment")
        new_recommendations = client.get(
            "/recommendations/99921-58-10-7").json()
    expected_new_recommendations = copy.deepcopy(existing_recommendations)
    for recommendantion in expected_new_recommendations:
        if "99921-58-10-7" in recommendantion["books"] and "0-9752298-0-X" in recommendantion["books"]:
            recommendantion["comments"].append(
                {"author": "username", "comment": "comment", "score": 0})
    # Then
    assert_that(existing_recommendations).is_not_equal_to(new_recommendations)
    assert_that(response.status_code).is_equal_to(201)
    assert_that(response.headers["location"]).is_equal_to(
        "/recommendations/99921-58-10-7/0-9752298-0-X/username")
    assert_that(new_recommendations).is_equal_to(expected_new_recommendations)


def test_recommendations_from_library():
    # Given
    expected_recommendaitons = [
        [book_list[1].to_dict(), 15], [book_list[2].to_dict(), 15], [book_list[3].to_dict(), 5], [book_list[4].to_dict(), 0]]

    # When
    with TestClient(mmr) as client:
        response = client.get("/recommendations/user2/generic")

    # Then
    check_response(response, 200, expected_recommendaitons)


def test_recommendations_from_library_not_found():
    # Given
    expected_response = {"error": "Library or user not found"}

    # When
    with TestClient(mmr) as client:
        response = client.get(
            "/recommendations/ThisUserDoesNotExist/IMadeThisUp")

    # Then
    check_response(response, 404, expected_response)
