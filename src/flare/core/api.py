#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

from dataclasses import dataclass
from typing import List

import requests


@dataclass
class Cache:
    """Represents a client-side cache of, e.g., users so redundant network requests do not have to be made."""

    users: dict[int, dict]

    def __init__(self):
        self.users = {}


class FlarumAPI:
    """Responsible for making outgoing requests to a Flarum server's given rest API endpoints."""

    endpoint: str
    cache: Cache

    def __init__(self, endpoint: str):
        if not endpoint.endswith("/api"):
            raise ValueError("The Flarum API endpoint must end with /api")
        if not endpoint.startswith("https://"):
            raise ValueError("We want HTTPS nowadays!")

        self.endpoint = endpoint
        self.cache = Cache()

    def discussions(self) -> dict:
        """List all discussions."""

        response = requests.get(f"{self.endpoint}/discussions")
        return response.json()

    def discussion(self, slug: str) -> dict:
        """Get specified discussion by its URL slug."""

        response = requests.get(
            f"{self.endpoint}/discussions/{slug}", params={"bySlug": True}
        )
        return response.json()

    def posts(self, ids: List[str]) -> dict:
        """Get all posts by their respective ids."""

        response = requests.get(
            # We are forced to do this ugly method of putting a string instead of a
            # dictionary into `params` because `requests` otherwise encodes those.
            # Which, normally, is a good thing, but Flarum does not like the query
            # parameters being encoded here for some reason...
            f"{self.endpoint}/posts",
            params=f"filter[id]={",".join(ids)}",
        )

        return response.json()

    def user(self, uid: int) -> dict:
        """Get a specific user by user id."""

        if uid in self.cache.users:
            return self.cache.users[uid]

        response = requests.get(f"{self.endpoint}/users/{uid}")
        json = response.json()

        self.cache.users[uid] = json
        return json
