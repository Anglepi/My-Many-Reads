from user_recommendation import UserRecommendation
from assertpy import assert_that


def test_recommendation_equality():
    # Given - When
    recommendation1 = UserRecommendation(
        ("book_id1", "book_id2"), UserRecommendation.UserComment("userA", "Both are cool"))
    recommendation2 = UserRecommendation(
        ("book_id2", "book_id1"), UserRecommendation.UserComment("userB", "Both are entertainning"))
    recommendation3 = UserRecommendation(
        ("book_id5", "book_id1"), UserRecommendation.UserComment("userC", "Both are scary"))

    # Then
    assert_that(recommendation1).is_equal_to(recommendation2)
    assert_that(recommendation1).is_not_equal_to(recommendation3)
    assert_that(recommendation1).is_not_equal_to("potatoes")


def test_recommendation_dict():
    # Given
    recommendation1 = UserRecommendation(
        ("book_id1", "book_id2"), UserRecommendation.UserComment("userA", "Both are cool"))
    expected_dict = {"books": ["book_id1", "book_id2"], "comments": [
        {"author": "userA", "comment": "Both are cool", "score": 0}]}

    # When
    recommendation_dict = recommendation1.to_dict()

    # Then
    assert_that(recommendation_dict).is_equal_to(expected_dict)


def test_add_comment():
    # Given
    recommendation = UserRecommendation(
        ("book_id1", "book_id2"), UserRecommendation.UserComment("userA", "Both are cool"))
    new_comment = UserRecommendation.UserComment(
        "userB", "Both are entertainning")
    expected_dict = {"books": ["book_id1", "book_id2"], "comments": [
        {"author": "userA", "comment": "Both are cool", "score": 0},
        {"author": "userB", "comment": "Both are entertainning", "score": 0}]}

    # When
    recommendation.add_comment(new_comment)

    # Then
    assert_that(recommendation.to_dict()).is_equal_to(expected_dict)


def test_cannot_add_multiple_comments():
    # Given
    recommendation = UserRecommendation(
        ("book_id1", "book_id2"), UserRecommendation.UserComment("userA", "Both are cool"))
    new_comment = UserRecommendation.UserComment(
        "userA", "Both are entertainning")
    expected_dict = {"books": ["book_id1", "book_id2"], "comments": [
        {"author": "userA", "comment": "Both are cool", "score": 0}]}

    # When
    recommendation.add_comment(new_comment)

    # Then
    assert_that(recommendation.to_dict()).is_equal_to(expected_dict)


def test_has_book():
    # Given
    recommendation = UserRecommendation(
        ("book_id1", "book_id2"), UserRecommendation.UserComment("userA", "Both are cool"))

    # When - Then
    assert_that(recommendation.has_book("book_id1")).is_true()
    assert_that(recommendation.has_book("book_id4")).is_false()


def test_get_author_comments():
    # Given
    user_comment = UserRecommendation.UserComment("userA", "Both are cool")
    recommendation = UserRecommendation(
        ("book_id1", "book_id2"), user_comment)

    # When - Then
    assert_that(recommendation.get_author_comments("userA")[
                0].to_dict()).is_equal_to(user_comment.to_dict())
    assert_that(recommendation.get_author_comments("NonExistent")).is_empty()


def test_vote_comment():
    # Given
    recommendation = UserRecommendation(
        ("book_id1", "book_id2"), UserRecommendation.UserComment("userA", "Both are cool"))
    expected_dict = {"books": ["book_id1", "book_id2"], "comments": [
        {"author": "userA", "comment": "Both are cool", "score": 1}]}

    # When
    recommendation.vote_comment("userA")
    recommendation.vote_comment("userB")

    # Then
    assert_that(recommendation.to_dict()).is_equal_to(expected_dict)
