# anarchists_cookbook/resources/__init__.py
from dagster import Definitions, load_assets_from_package_module
from .reddit_resource import reddit_client_resource
import anarchists_cookbook.assets as assets_package

defs = Definitions(
    assets=load_assets_from_package_module(assets_package),
    resources={
        "reddit_client": reddit_client_resource,
    },
)