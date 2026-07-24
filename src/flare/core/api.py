from typing import List
from dataclasses import dataclass

import requests

@dataclass
class ListDiscussionsResponse:
    discussions: List


@dataclass
class GetDiscussionResponse:
    pass


class FlarumAPI:
    endpoint: str

    def __init__(self, endpoint: str):
        if not endpoint.endswith("/api"):
            raise ValueError("The Flarum API endpoint must end with /api")
        if not endpoint.startswith("https://"):
            raise ValueError("We want HTTPS nowadays!")

        self.endpoint = endpoint

    def list_discussions(self) -> ListDiscussionsResponse:
        response = requests.get(f"{self.endpoint}/discussions")
        pass

    def get_discussion(self, path: str) -> GetDiscussionResponse:
        response = requests.get(f"{self.endpoint}/discussions/{path}")
        pass
