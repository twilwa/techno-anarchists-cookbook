# import pytest
# import os
# import csv
# from unittest.mock import MagicMock, patch
# from praw.models import Subreddit, Submission, Comment
# from dagster import build_op_context, materialize_to_memory, materialize

# from anarchists_cookbook.resources.reddit_resource import RedditResource
# from anarchists_cookbook.assets import reddit_posts_data, reddit_posts_csv

# @pytest.fixture
# def mock_reddit_client():
    # mock_reddit_client = MagicMock()
    # mock_subreddit = MagicMock(spec=Subreddit)

    # mock_author1 = MagicMock()
    # mock_author1.name = "Test Author 1"

    # mock_author2 = MagicMock()
    # mock_author2.name = "Test Author 2"

    # mock_comment1 = MagicMock(spec=Comment)
    # mock_comment1.body = "Test Comment 1"
    # mock_comment1.score = 10
    # mock_comment1.author = mock_author1

    # mock_comment2 = MagicMock(spec=Comment)
    # mock_comment2.body = "Test Comment 2"
    # mock_comment2.score = 20
    # mock_comment2.author = mock_author2

    # mock_submission1 = MagicMock(spec=Submission)
    # mock_submission1.title = "Test Post 1"
    # mock_submission1.url = "https://test.com/post1"
    # mock_submission1.score = 100
    # mock_submission1.num_comments = 10
    # mock_submission1.selftext = "Test Post 1 Content"
    # mock_submission1.comments = MagicMock()
    # mock_submission1.comments.__iter__.return_value = [mock_comment1, mock_comment2]

    # mock_submission2 = MagicMock(spec=Submission)
    # mock_submission2.title = "Test Post 2"
    # mock_submission2.url = "https://test.com/post2"
    # mock_submission2.score = 200
    # mock_submission2.num_comments = 20
    # mock_submission2.selftext = "Test Post 2 Content"
    # mock_submission2.comments = MagicMock()
    # mock_submission2.comments.__iter__.return_value = []

    # mock_subreddit.controversial.return_value = [mock_submission1]
    # mock_subreddit.top.return_value = [mock_submission2]
    # mock_subreddit.hot.return_value = []
    # mock_reddit_client.subreddit.return_value = mock_subreddit

    # return mock_reddit_client

# @pytest.fixture
# def mock_context(mock_reddit_client):
    # return build_op_context(
        # resources={"reddit_client": mock_reddit_client}
    # )
# def test_reddit_assets():
    # # Arrange
    # resources = {"reddit_client": RedditResource()}

    # # Act
    # result = materialize_to_memory(
        # [reddit_posts_data, reddit_posts_csv],
        # resources=resources,
    # )

    # # Assert
    # assert result.success

    # data = result.output_for_node("reddit_posts_data")
    # assert len(data) == 30

    # # Assert post content
    # for post in data:
        # assert isinstance(post["title"], str)
        # assert isinstance(post["url"], str)
        # assert isinstance(post["score"], int)
        # assert isinstance(post["num_comments"], int)
        # assert isinstance(post["selftext"], str)

    # # Assert comment trees
    # total_comments = 0
    # for post in data:
        # comments = post["comments"]
        # assert len(comments) <= 10
        # total_comments += len(comments)

        # for comment in comments:
            # assert isinstance(comment["author"], (str, type(None)))
            # assert isinstance(comment["body"], str)
            # assert isinstance(comment["score"], int)



    # file_path = result.output_for_node("reddit_posts_csv")
    # assert file_path.startswith("reddit_data_")
    # assert file_path.endswith(".csv")
    # with open(file_path, "r") as file:
        # reader = csv.DictReader(file)
        # rows = list(reader)
        # assert len(rows) == 30

# def test_reddit_posts_csv(mock_context, tmp_path):
    # # Arrange
    # context = MagicMock()
    # context.resources.reddit_client.client.return_value = mock_reddit_client
    # data = [
        # {
            # "title": "Test Post 1",
            # "url": "https://test.com/post1",
            # "score": 100,
            # "num_comments": 10,
            # "selftext": "Test Post 1 Content",
            # "comments": [
                # {
                    # "author": "Test Author 1",
                    # "body": "Test Comment 1",
                    # "score": 10,
                # },
                # {
                    # "author": "Test Author 2",
                    # "body": "Test Comment 2",
                    # "score": 20,
                # },
            # ],
        # },
        # {
            # "title": "Test Post 2",
            # "url": "https://test.com/post2",
            # "score": 200,
            # "num_comments": 20,
            # "selftext": "Test Post 2 Content",
            # "comments": [],
        # },
    # ]

    # # Act
    # file_path = reddit_posts_csv(mock_context, data)

    # # Assert
    # assert file_path.startswith("reddit_data_")
    # assert file_path.endswith(".csv")
    # with open(file_path, "r") as file:
        # reader = csv.DictReader(file)
        # rows = list(reader)
        # assert len(rows) == 2
        # assert isinstance(rows[0]["title"], str)
        # assert isinstance(rows[1]["title"], str)
