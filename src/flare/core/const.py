#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

from dataclasses import dataclass
from typing import List


@dataclass
class User:
    """Metadata of a Flarum forum user."""

    username: str
    id: int

    def __init__(
        self,
        /,
        username: str | None = None,
        identifier: int | None = None,
        deleted: bool = False,
    ):
        if deleted:
            self.username = "[deleted]"
            self.id = -1
        else:
            # We must assume the consumer implicitly just passes None to these below
            # only when they use the `deleted` parameter.
            assert username is not None
            assert identifier is not None

            self.username = username
            self.id = identifier


@dataclass
class Post:
    """Metadata of a Flarum post."""

    text: str
    author: User
    likes: int
    id: int


@dataclass
class Discussion:
    """Metadata of a Flarum discussion."""

    title: str
    author: User
    posts: List[Post]
    """Post objects may not be loaded, use the `post_ids` property below for use in loading them"""

    slug: str

    post_ids: List[str]
    """All post IDs are always loaded (assuming that Flare.discussion() has been called), unlike the `posts` property."""
