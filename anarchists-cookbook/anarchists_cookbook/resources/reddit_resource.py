import os
from dagster import ConfigurableResource
from dotenv import load_dotenv
import praw

load_dotenv()

class RedditResource(ConfigurableResource):
    client_id: str = os.getenv("REDDIT_CLIENT_ID")
    client_secret: str = os.getenv("REDDIT_CLIENT_SECRET") 
    user_agent: str = "scrapeyboi"
    username: str = os.getenv("REDDIT_USERNAME")
    password: str = os.getenv("REDDIT_PASSWORD")

    def client(self):
        return praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
            username=self.username,
            password=self.password,
        )