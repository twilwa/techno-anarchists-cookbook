# reddit_data.py
from dagster import op, get_dagster_logger, AssetMaterialization

@op(required_resource_keys={"reddit_client"})
def fetch_reddit_data(context):
    logger = get_dagster_logger()
    reddit_client = context.resources.reddit_client.client()
    subreddit_name = context.op_config["subreddit"]

    logger.info(f"Fetching data from subreddit: {subreddit_name}")
    subreddit = reddit_client.subreddit(subreddit_name)

    data = []
    for post in subreddit.hot(limit=10):
        data.append({
            "title": post.title,
            "url": post.url,
            "score": post.score,
            "num_comments": post.num_comments
        })

    return data