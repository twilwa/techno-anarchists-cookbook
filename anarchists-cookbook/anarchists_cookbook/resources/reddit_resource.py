from pydantic import BaseModel
from dagster import resource, Field, StringSource
import praw

class RedditClientConfig(BaseModel):
    client_id: str
    client_secret: str
    user_agent: str
    username: str
    password: str

@resource({
    "client_id": Field(StringSource),
    "client_secret": Field(StringSource),
    "user_agent": Field(StringSource),
    "username": Field(StringSource),
    "password": Field(StringSource),
})
def reddit_client_resource(init_context):
    config = RedditClientConfig(**init_context.resource_config)
    # Initialize the praw Reddit client with the config
    return praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
        username=config.username,
        password=config.password,
    )