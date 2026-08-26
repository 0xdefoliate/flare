#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

from html.parser import HTMLParser


class FlareHTMLParser(HTMLParser):
    """An HTML "parser" which is adapted to output contents in a terminal environment."""

    output: str

    def __init__(self):
        super().__init__()
        self.output = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        match tag:
            case "br":
                self.output += "\n"

    def handle_data(self, data: str) -> None:
        self.output += f"{data.strip()}\n"
