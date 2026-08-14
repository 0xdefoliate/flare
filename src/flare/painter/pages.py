#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

from typing import List, Any

from flare.core.const import User, Discussion
from flare.painter.html import FlareHTMLParser
from flare.painter.util import clear_screen


class Page:
    title: str

    def __init__(self, title: str):
        self.title = title

    def render(self) -> Any:
        clear_screen()
        print(self.title)
        print("=" * len(self.title))
        print()


class MainPage(Page):
    """This is the landing page, i.e. the page which gets rendered after starting flare."""

    discussions: List[Discussion]

    def __init__(self, server: str, discussions: List[Discussion]):
        super().__init__(f"Welcome to {server}!")
        self.discussions = discussions

    def render(self) -> int:
        super().render()

        for i, discussion in enumerate(self.discussions):
            print(f"  [{i}] {discussion.title}")

        rv: int
        try:
            rv = int(input(": "))
        except ValueError:
            rv = -1

        return rv


class UserPage(Page):
    """A page for a specific user, not used currently."""

    def __init__(self, user: User):
        super().__init__(f"@{user.username}")

    def render(self) -> None:
        super().render()


class DiscussionPage(Page):
    """A page shown for a specific discussion (i.e. thread)"""

    discussion: Discussion
    parser: FlareHTMLParser

    def __init__(self, discussion: Discussion):
        super().__init__(f"Discussion: {discussion.title}")
        self.discussion = discussion
        self.parser = FlareHTMLParser()

    def render(self) -> bool:
        super().render()

        for post in self.discussion.posts:
            print(f"\033[1m@{post.author.username}\033[0m:")
            self.parser.feed(post.text)
            print()
            print()

        return input(": ") != "q"
