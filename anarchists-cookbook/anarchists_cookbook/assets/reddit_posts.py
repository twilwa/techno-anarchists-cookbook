import csv
from datetime import datetime
from dagster import Config, asset, AssetMaterialization
from .resources import reddit_client_resource, RedditClientConfig

@asset(required_resource_keys={"reddit_client"}, group_name="reddit" config: RedditClientConfig)
def reddit_posts_data(context):
    reddit_client = context.resources.reddit_client
    subreddit_name = "LocalLlama"
    limit = 10  # Fetch 10 posts for each sort type

    subreddit = reddit_client.subreddit(subreddit_name)
    context.log.info(f"reddit_client type: {type(reddit_client)}")
    data = []

    for sort_type in ["controversial", "top", "hot"]:
        for post in getattr(subreddit, sort_type)(limit=limit):
            post_data = {
                "title": post.title,
                "url": post.url,
                "score": post.score,
                "num_comments": post.num_comments,
                "selftext": post.selftext,
            }
            
            comments_data = []
            post.comments.replace_more(limit=None)
            for comment in post.comments[:10]:
                comment_data = {
                    "author": comment.author.name if comment.author else None,
                    "body": comment.body,
                    "score": comment.score,
                }
                comments_data.append(comment_data)
            
            post_data["comments"] = comments_data
            data.append(post_data)

    yield AssetMaterialization(
        asset_key="reddit_posts_data",
        metadata={
            "subreddit": subreddit_name,
            "num_posts": len(data),
            "sort_types": ["controversial", "top", "hot"],
        },
    )

    return data

@asset(required_resource_keys={"reddit_client"}, group_name="reddit")
def reddit_posts_csv(context, reddit_posts_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"reddit_data_{timestamp}.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["title", "url", "score", "num_comments", "selftext", "comments"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reddit_posts_data)

    return file_path