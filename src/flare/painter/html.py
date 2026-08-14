#  Copyright (c) 2026 Axel H. Karlsson and contributors.
#
#  You may use the source-code in accordance with the licence found
#  in the LICENSE file, available in the project's root directory.

from html.parser import HTMLParser


class FlareHTMLParser(HTMLParser):
    """An HTML "parser" which is adapted to output contents in a terminal environment.
    It is not really a parser in the classical sense, but more of an interpreter printing to
    stdout depending on what tags it stumbles upon."""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        match tag:
            case "br":
                print()

    def handle_data(self, data: str) -> None:
        print(f"   {data.strip()}")
