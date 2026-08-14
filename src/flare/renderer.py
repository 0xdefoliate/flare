#!/usr/bin/env python3

#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

import sys
from dataclasses import dataclass

from flare.core.const import Discussion
from flare.core.flare import Flare
from flare.painter.pages import MainPage, DiscussionPage
from flare.painter.util import clear_screen


@dataclass
class DiscussionLoader:
    """Manages lazy loading a given discussion and keeps track of what's been loaded."""

    discussion: Discussion
    flare: Flare

    counter: tuple[int, int]
    step: int

    def __init__(self, flare: Flare, discussion: Discussion, step: int = 4):
        self.counter = (0, step)
        self.step = step

        self.flare = flare
        self.discussion = discussion

    def maybe_load_first(self) -> None:
        if self.counter[0] > 0:
            return

        try:
            to_load = [self.discussion.post_ids[0]]
        except IndexError:
            return

        post = self.flare.posts(to_load)

        self.discussion.posts.extend(post)

        # we have read one post, so update the counter.
        self.counter = (1, self.step + 1)

    def load_more(self) -> None:
        start = self.counter[0]
        end = (
            -1 if self.counter[1] >= len(self.discussion.post_ids) else self.counter[1]
        )

        if start >= len(self.discussion.post_ids):
            return

        to_load = self.discussion.post_ids[start:end]
        posts = self.flare.posts(to_load)

        self.discussion.posts.extend(posts)
        self.counter = (self.counter[0] + self.step, self.counter[1] + self.step)


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

    main_page = MainPage(server, discussions)

    # The `main_page.render()` method returns an integer, which is the
    # index of a given discussion in `discussions`, if non-zero, it means
    # that the user didn't provide an integer, and the program will end.
    #
    # In other words, it will keep rendering the main page as a side effect
    # until the user stops entering a valid integer.
    while (index := main_page.render()) >= 0:
        try:
            loader = DiscussionLoader(flare, discussions[index], step=2)
        except IndexError:
            continue

        flare.update_discussion(loader.discussion)
        loader.maybe_load_first()  # load the first thread post (OP's post)

        discussion_page = DiscussionPage(loader.discussion)

        # This loop runs while the user keeps entering any key (which isn't "q").
        while discussion_page.render():
            loader.load_more()

    clear_screen()


if __name__ == "__main__":
    renderer()
