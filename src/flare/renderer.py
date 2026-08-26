#!/usr/bin/env python3

#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

import sys
from dataclasses import dataclass
from typing import List, Any, Callable

from flare.core.const import Discussion, Post
from flare.core.flare import Flare
from flare.ui.components import Header, ScrollableList, ScrollableListCallback
from flare.ui.core import Screen, Page, Text, Navigator
from flare.ui.html import FlareHTMLParser


@dataclass
class ApplicationState:
    server: str
    discussions: List[Discussion]
    posts: List[Post]

    update_discussions: Callable[[ApplicationState], None]
    update_posts: Callable[[ApplicationState, Discussion], None]


def reflect_scroll_indicator(y: int, header: Header, screen: Screen) -> None:
    if y > 0:
        header.indicator = "[SCROLL]"
    else:
        header.indicator = None

    header.render(screen)

    screen.refresh([header])


class DiscussionPage(Page):
    app: ApplicationState

    discussion: Discussion

    header: Header
    select: ScrollableList

    class Callback(ScrollableListCallback):
        def __init__(self, data: dict[str, Any]):
            self.data = data

        def on_quit(self) -> bool:
            self.data["page"].navigator.restart()
            return True

        def on_select(self, index: int) -> bool:
            return False

        def on_scroll(self, y: int) -> None:
            reflect_scroll_indicator(
                y, self.data["page"].header, self.data["page"].screen
            )

    def __init__(
        self,
        screen: Screen,
        discussion: Discussion,
        app: ApplicationState,
        navigator: Navigator,
    ):
        super().__init__(screen, [], navigator)

        self.discussion = discussion
        self.app = app

        self.header = Header(Text(discussion.title))

        self.select = ScrollableList(
            items=[],
            callbacks=self.Callback({"page": self}),
        )

        self.areas = [self.header, self.select]

    def render(self) -> None:
        self.app.update_posts(self.app, self.discussion)
        self.select.clean()

        posts = []

        i = 0
        for entry in self.discussion.posts:
            parser = FlareHTMLParser()
            parser.feed(entry.text)

            output = parser.output
            output = f"%B{entry.author.username}:%b\n{output.strip()}"

            posts.append(output)

            i += 1

        post_heights = [str(item).count("\n") for item in posts]
        height: int = 0

        for post_height in post_heights:
            height += post_height

        self.select = ScrollableList(
            items=[post + "\n\n" for post in posts if post != ""],
            callbacks=self.Callback({"page": self}),
        )

        self.areas = [self.header, self.select]

        super().render()


class MainPage(Page):
    app: ApplicationState

    header: Header
    select: ScrollableList

    navigator: Navigator

    title: Text
    indicator: str | None

    class Callback(ScrollableListCallback):
        def __init__(self, data: dict[str, Any]):
            self.data = data

        def on_quit(self) -> bool:
            self.data["page"].screen.destroy()
            sys.exit(0)

        def on_select(self, index: int) -> bool:
            discussion = self.data["page"].app.discussions[index]

            self.data["page"].navigator.navigate(
                to=DiscussionPage(
                    screen=self.data["page"].screen,
                    discussion=discussion,
                    app=self.data["page"].app,
                    navigator=self.data["page"].navigator,
                )
            )

            return True

        def on_scroll(self, y: int) -> None:
            reflect_scroll_indicator(
                y, self.data["page"].header, self.data["page"].screen
            )

    def __init__(self, screen: Screen, app: ApplicationState):
        super().__init__(screen, [], Navigator(self, screen))

        self.app = app

        self.title = Text(f"Welcome to %B{self.app.server}%b!")
        self.indicator = None

        self.header = Header(self.title)

        self.select = ScrollableList(
            items=[discussion.title for discussion in app.discussions],
            callbacks=self.Callback({"page": self}),
            selectable=True,
        )

        self.areas = [self.header, self.select]


def renderer() -> None:
    """This is the actual program entrypoint, where it (hopefully) is sandboxed."""

    args = sys.argv[1:]

    if len(args) < 1:
        print(
            "No Flarum origin provided, please provide it as a command-line argument!"
        )
        return sys.exit(1)

    server = args[0]
    flare = Flare(server)
    discussions = flare.discussions()

    screen = Screen()

    def update_discussions(state: ApplicationState) -> None:
        # no-op for now.
        pass

    def update_posts(state: ApplicationState, discussion: Discussion) -> None:
        flare.update_discussion(discussion)
        discussion.posts = flare.posts(discussion.post_ids)

    state = ApplicationState(
        server,
        discussions=discussions,
        posts=[],
        update_discussions=update_discussions,
        update_posts=update_posts,
    )

    main_page = MainPage(screen, state)
    main_page.render()


if __name__ == "__main__":
    renderer()
