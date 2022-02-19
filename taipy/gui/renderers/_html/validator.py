import typing as t
import warnings
from html.parser import HTMLParser

from ...utils.stack import Stack
from .. import PageValidator


class HTMLValidator(PageValidator):
    def generate_error_detail(self) -> str:
        base = f"HTML validation error on line {self._line + 1}"
        if hasattr(self._page, "_filepath"):
            base += f" in file {self._page._filepath}"
        return base

    def validate(self) -> bool:
        parser = _HTMLValidator()
        while self.has_next_line():
            parser.feed(self.get_line())
            parser.warn(self.generate_error_detail())
            self._line += 1
        return not parser._has_warned


class _HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self._tags = Stack()
        self._has_warned = False
        self._warning_list = []

    def handle_starttag(self, tag, props) -> None:
        self._tags.push(tag)

    def handle_data(self, data: str) -> None:
        pass

    def handle_endtag(self, tag) -> None:
        pass

    def warn(self, detail: str):
        for w in self._warning_list:
            warnings.warn(f"{detail}: {w}")
        self._warning_list.clear()
