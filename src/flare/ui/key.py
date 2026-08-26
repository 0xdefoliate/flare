#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.
from enum import Enum, auto


class Key(Enum):
    ENTER = auto()
    TAB = auto()
    SHIFT_TAB = auto()
    ARROW_UP = auto()
    ARROW_DOWN = auto()
    QUIT = auto()


def get_key(value: str) -> Key | str:
    try:
        if ord(value) == 10:
            return Key.ENTER
        if ord(value) == 9:
            return Key.TAB
    except TypeError:
        pass

    if value == "KEY_BTAB":
        return Key.SHIFT_TAB
    if value == "KEY_UP":
        return Key.ARROW_UP
    if value == "KEY_DOWN":
        return Key.ARROW_DOWN

    # 27 here means ESC.
    if ord(value) == 27 or value == "q":
        return Key.QUIT

    return value
