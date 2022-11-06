from user_recommendation import UserRecommendation
from assertpy import assert_that


def test_recommendation_equality():
    recommendation1 = UserRecommendation(
        ("ISBN1", "ISBN2"), UserRecommendation.UserComment("userA", "Both are cool"))
    recommendation2 = UserRecommendation(
        ("ISBN2", "ISBN1"), UserRecommendation.UserComment("userB", "Both are entertainning"))
    recommendation3 = UserRecommendation(
        ("ISBN5", "ISBN1"), UserRecommendation.UserComment("userC", "Both are scary"))

    assert_that(recommendation1).is_equal_to(recommendation2)
    assert_that(recommendation1).is_not_equal_to(recommendation3)


def test_recommendation_dict():
    recommendation1 = UserRecommendation(
        ("ISBN1", "ISBN2"), UserRecommendation.UserComment("userA", "Both are cool"))
    recommendation_dict = recommendation1.to_dict()
    expected_dict = {"books": ["ISBN1", "ISBN2"], "comments": [
        {"author": "userA", "comment": "Both are cool", "score": 0}]}

    assert_that(recommendation_dict).is_equal_to(expected_dict)