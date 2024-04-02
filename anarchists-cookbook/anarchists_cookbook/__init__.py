from dagster import Definitions, load_assets_from_modules
from .assets import reddit_posts 
from .resources import reddit_resource# Assuming this is the module with your assets

defs = Definitions(
    assets=load_assets_from_modules([reddit_posts]),  # Note the list brackets
    resources={
        "reddit_client": reddit_resource.reddit_client_resource,
    },
)