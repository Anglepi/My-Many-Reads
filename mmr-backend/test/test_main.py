from assertpy import assert_that
from fastapi.testclient import TestClient
from main import mmr

client = TestClient(mmr)


def check_response(response, status, body):
    assert_that(response.status_code).is_equal_to(status)
    assert_that(response.json()).is_equal_to(body)


def test_api_initialized():
    response = client.get("/")
    expected_status = 200
    expected_body = {"message": "Hello World!"}

    check_response(response, expected_status, expected_body)
