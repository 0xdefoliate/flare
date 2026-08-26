#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

import curses
from dataclasses import dataclass
from typing import List, Any

COLOUR_PAIR_BLUE_FG = 1


@dataclass
class Position:
    x: int
    y: int


class Screen:
    """Manages the lifecycle and initialisation of the `ncurses` app overall."""

    screen: curses.window

    def __init__(self):
        self.screen = curses.initscr()
        self.screen.keypad(True)

        curses.noecho()
        curses.curs_set(0)
        curses.cbreak()

        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(COLOUR_PAIR_BLUE_FG, curses.COLOR_BLUE, -1)

    def destroy(self) -> None:
        self.screen.keypad(False)

        curses.nocbreak()
        curses.curs_set(1)
        curses.echo()

        curses.endwin()

    @staticmethod
    def refresh(areas: List[Area]) -> None:
        """Prepares given areas for displaying, but doesn't perform it; use the `update()` method for that."""
        for area in areas:
            if isinstance(area, Window):
                area._window.noutrefresh()
            else:
                assert isinstance(area, Pad)
                area.refresh()

    @staticmethod
    def update():
        """Commits staged refreshes onto the screen."""
        curses.doupdate()

    @staticmethod
    def width() -> int:
        return curses.COLS

    @staticmethod
    def height() -> int:
        return curses.LINES


class Navigator:
    """Facilitates and coordinates navigation to different pages."""

    start: Page
    current: Page
    screen: Screen

    def __init__(self, start: Page, screen: Screen):
        self.start = start
        self.current = start
        self.screen = screen

    def navigate(self, to: Page) -> None:
        """Navigate to a given page in a proper way."""
        for area in self.current.areas:
            area.clean()
            self.screen.refresh([area])

        self.current = to
        self.current.render()

    def restart(self) -> None:
        """Navigate back to the first page."""
        self.navigate(self.start)


class Page:
    """Represents a portion of the app which is given the whole screen size."""

    screen: Screen
    areas: List[Area]
    navigator: Navigator

    def __init__(self, screen: Screen, areas: List[Area], navigator: Navigator):
        self.screen = screen
        self.areas = areas
        self.navigator = navigator

    def render(self) -> None:
        for area in self.areas:
            area.render(self.screen)
            self.screen.refresh([area])
            self.screen.update()


class Area:
    """A common ground for both windows and pads."""

    _window: curses.window

    def __init__(self, _window: curses.window):
        self._window = _window
        self._window.keypad(True)

    def render(self, screen: Screen) -> Any:
        """Draws content onto the area, but doesn't commit it directly."""
        raise NotImplementedError

    def write(self, at: Position, text: Text) -> tuple[str, Position]:
        """Write text at given position."""

        self._window.move(at.y, at.x)
        self._window.clrtobot()
        return text.render(self)

    def clean(self) -> None:
        """Completely erase all contents of the area; used when deallocating the area."""
        self._window.clear()


class Window(Area):
    """High-level abstraction of an `ncurses` window."""

    x: int
    y: int
    width: int
    height: int

    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(curses.newwin(height, width, y, x))

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self, screen: Screen) -> None:
        raise NotImplementedError


class Pad(Area):
    """High-level abstraction of an `ncurses` pad."""

    width: int
    height: int

    def __init__(self, width: int, height: int):
        super().__init__(curses.newpad(height, width))

        self.width = width
        self.height = height

    def render(self, screen: Screen) -> None:
        raise NotImplementedError

    def refresh(self) -> None:
        raise NotImplementedError


class Text:
    """High-level component for rendering text; manages styling, text overflows, etc."""

    text: str

    _parent: Area

    def __init__(self, text: str):
        self.text = text

    def render(self, parent: Area) -> tuple[str, Position]:
        self._parent = parent
        y, x = parent._window.getyx()

        position = 0
        output = ""
        state = curses.A_NORMAL
        previous_state = curses.A_NORMAL

        bound_y, bound_x = parent._window.getmaxyx()

        boundaries = Position(bound_x, bound_y)
        start = Position(x, y)

        while position < len(self.text):
            character = self.text[position]
            try:
                next_character = self.text[position + 1]
            except IndexError:
                next_character = None
            try:
                next_next_character = self.text[position + 2]
            except IndexError:
                next_next_character = None

            if character == "%" and next_character == "B":
                previous_state = state
                state = curses.A_BOLD
                position += 2
                continue

            if character == "%" and next_character == "b":
                state = previous_state
                position += 2
                continue

            if character == "%" and next_character == "C":
                previous_state = state

                match next_next_character:
                    case "b":
                        state = curses.color_pair(COLOUR_PAIR_BLUE_FG)

                position += 3
                continue

            if character == "%" and next_character == "c":
                state = previous_state
                position += 2

                continue

            if x >= boundaries.x:
                x = start.x
                y += 1

            if character == "\n":
                x = start.x
                y += 1

                output += character
                position += 1

                continue

            parent._window.addch(
                y,
                x,
                character,
                state,
            )

            output += character
            position += 1
            x += 1

        self._parent._window.move(y, x)
        return output, Position(x, y)
