#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.
import requests.utils
from typing import List

from flare.core.api import FlarumAPI
from flare.core.const import Discussion, User, Post


class Flare:
    """Primary class intended for external consumption."""

    origin: str
    endpoint: str

    api: FlarumAPI

    def __init__(self, origin: str):
        self.origin = origin
        self.endpoint = f"https://{origin}/api"

        self.api = FlarumAPI(self.endpoint)

    def discussions(self) -> List[Discussion]:
        rv = []
        discussions = self.api.discussions()

        for discussion in discussions["data"]:
            rv.append(
                Discussion(
                    title=discussion["attributes"]["title"],
                    author=User(
                        username="",
                        identifier=discussion["relationships"]["user"]["data"]["id"],
                    ),
                    posts=[],
                    slug=discussion["attributes"]["slug"],
                    post_ids=[],
                )
            )

        return rv

    def update_discussion(self, discussion: Discussion) -> None:
        """Mutates a given `Discussion` to include additional metadata not included in `Flare.discussions()`."""

        _discussion = self.api.discussion(discussion.slug)

        discussion.post_ids = [
            entry["id"]
            for entry in _discussion["data"]["relationships"]["posts"]["data"]
            if entry["type"] == "posts"
        ]

    def user(self, identifier: int) -> User:
        user = self.api.user(identifier)

        return User(
            username=user["data"]["attributes"]["username"],
            identifier=user["data"]["id"],
        )

    def posts(self, ids: List[str]) -> List[Post]:
        _posts = self.api.posts(ids)
        posts = sorted(
            [post for post in _posts["data"]],
            key=lambda entry: entry["attributes"]["number"],
        )

        # We process the posts again to transform it into a suitable data structure,
        # and also to handle edge-cases, (i.e. a [deleted] user, etc.).

        rv = []

        for post in posts:
            text = post.get("attributes").get("contentHtml", "")
            author: User

            # check if user is [deleted].
            if "user" not in post["relationships"]:
                author = User(deleted=True)
            else:
                author = self.user(post["relationships"]["user"]["data"]["id"])

            rv.append(
                Post(
                    text=text,
                    author=author,
                    id=post["id"],
                    likes=0,  # likes are not implemented yet, so, we hard-code it for now.
                )
            )

        return rv
