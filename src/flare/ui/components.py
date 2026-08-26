#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.
import curses
from typing import List, Protocol, Any

from flare.ui.core import Screen, Window, Text, Pad, Position
from flare.ui.key import get_key, Key

TEMPORARY_HEIGHT = 3999  # rows


class ScrollableListCallback(Protocol):
    """A protocol which defines possible callback handlers for a `ScrollableList`."""

    # TODO: Use normal class-level properties instead of this shit.
    data: dict[str, Any]

    def on_quit(self) -> bool:
        pass

    def on_select(self, index: int) -> bool:
        pass

    def on_scroll(self, y: int) -> None:
        pass


class Header(Window):
    """Represents a row at the top of a window which displays a title and, optionally, an indicator."""

    title: Text
    indicator: str | None

    def __init__(self, title: Text, indicator: str | None = None):
        super().__init__(x=0, y=0, width=curses.COLS, height=1)

        self.title = title
        self.indicator = indicator

    def render(self, screen: Screen) -> None:
        self._window.clrtoeol()
        self._window.bkgdset(" ", curses.A_STANDOUT)

        self._window.move(0, 0)
        for x in range(0, curses.COLS):
            self._window.insch(0, x, " ")

        self._window.move(0, 0)
        self._window.addch(" ")
        self._window.move(0, 1)

        # Do not crash the entire program if text overflows the screen.
        try:
            self.title.render(self)
        except curses.error:
            pass

        if self.indicator is None:
            return

        # add a whitespace before indicator begins to improve readability
        # in case of an overflow
        self._window.move(0, curses.COLS - len(self.indicator) - 1)
        self._window.insch(" ")

        # write indicator
        self._window.move(0, curses.COLS - len(self.indicator))
        self._window.insstr(0, curses.COLS - len(self.indicator), self.indicator)


class ScrollableList(Pad):
    """Represents a list which may scroll if necessary, and can have its items selected if enabled."""

    callbacks: ScrollableListCallback

    items: List[str]
    selected: int

    selectable: bool

    scroll_y: int
    max_scroll_y: int

    def __init__(
        self,
        items: List[str],
        callbacks: ScrollableListCallback,
        selectable: bool = False,
    ):
        super().__init__(
            width=curses.COLS, height=TEMPORARY_HEIGHT  # will be dynamically updated
        )
        self.items = items
        self.selected = 0
        self.selectable = selectable
        self.callbacks = callbacks
        self.scroll_y = 0
        self.max_scroll_y = 0  # this will be dynamically updated

    def _render_list(self) -> None:
        current_y = 2
        i = 0

        # Temporarily resize so exceptions complaining that ncurses
        # is drawing outside the bounds do not get caught during
        # the drawing process, because it doesn't reflect the
        # completed width and height.
        self._window.resize(TEMPORARY_HEIGHT, self.width)
        self._window.clear()

        # draw all list items one by one.
        for item in self.items:
            # only make the text bold when selected
            text = f"%B{item}%b" if self.selected == i and self.selectable else item

            _, p = self.write(Position(x=3, y=current_y), Text(text))
            current_y = p.y + 2

            i += 1

        # subtract by the amount of rows (+ padding) so that a whole
        # screen's worth of whitespace isn't present when scrolling
        # beyond actual contents.
        self.max_scroll_y = current_y - curses.LINES + 1
        if self.max_scroll_y < 0:
            self.max_scroll_y = 0

        self.height = current_y

        self._window.resize(self.height, self.width)

        self.refresh()

    def render(self, screen: Screen) -> None:
        self._window.clear()
        self._render_list()
        screen.update()

        while key := get_key(self._window.getkey()):
            match key:
                case Key.ARROW_UP:
                    if self.scroll_y > 0:
                        self.scroll_y -= 1
                        self.callbacks.on_scroll(self.scroll_y)
                        self.refresh(self.scroll_y)
                case Key.ARROW_DOWN:
                    if self.scroll_y < self.max_scroll_y:
                        self.scroll_y += 1
                        self.callbacks.on_scroll(self.scroll_y)
                        self.refresh(self.scroll_y)
                case Key.QUIT:
                    if self.callbacks.on_quit():
                        break

            # The following keys are only supported on selectable lists.
            if self.selectable:
                match key:
                    case Key.TAB | Key.SHIFT_TAB:
                        if key == Key.TAB:
                            # Cycle forwards

                            if self.selected >= len(self.items) - 1:
                                self.selected = 0
                            else:
                                self.selected += 1
                        else:
                            # Cycle backwards

                            if self.selected <= 0:
                                self.selected = len(self.items) - 1
                            else:
                                self.selected -= 1

                        self._render_list()
                        self.refresh(self.scroll_y)
                    case Key.ENTER:
                        if self.callbacks.on_select(self.selected):
                            break

            screen.update()

    def refresh(self, y: int = 0) -> None:
        self._window.noutrefresh(y, 0, 1, 0, curses.LINES - 1, curses.COLS)
