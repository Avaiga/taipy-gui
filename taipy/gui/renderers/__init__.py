from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from os import path
from ._html import TaipyHTMLParser
from ._markdown import makeTaipyExtension


class PageRenderer(ABC):
    """
    The base class that transform template text to actual pages that can be
    displayed on a Web browser.

    When a page is requested to be displayed, it is transformed into HTML
    code that can be sent to the client. All control placeholders are
    replaced by the appropriate graphical component so you can display
    your application variables, and potentially interact with them.
    """

    def __init__(self, content: str) -> None:
        """Initializes a new PageRenderer with the indicated content.

        Args:
            content (string): The text content or the path to the file holding the text to be transformed.

        If `content` is a path to a readable file, the file is read entirely as the text template.
        """
        self._content: t.Union[None, str] = None
        self.__process_content(content)

    def __process_content(self, content: str) -> None:
        if path.exists(content) and path.isfile(content):
            with open(t.cast(str, content), "r") as f:
                self._content = f.read()
        else:
            self._content = content

    def set_content(self, content: str) -> None:
        self.__process_content(content)
    
    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def render(self) -> str:
        pass


class PageValidator(ABC):
    """
    This base class provide validation functionality to PageRenderer. This allow users to catch potential errors in runtime.
    """

    def __init__(self, page: PageRenderer) -> None:
        self._page = page
    
    @abstractmethod
    def validate(self) -> bool:
        pass

class EmptyPageRenderer(PageRenderer):

    def __init__(self) -> None:
        super().__init__("<PageContent />")
    
    def validate(self) -> bool:
        return "<PageContent />" in self._content

    def render(self) -> str:
        return str(self._content)


class Markdown(PageRenderer):
    """
    The page renderer for _Markdown_ text.
    """

    def __init__(self, content: str) -> None:
        """Initializes a new `Markdown` page renderer.

        Args:
            content (string): The text content or the path to the file holding the Markdown text to be transformed.
        """
        super().__init__(content)
    
    def validate(self) -> bool:
        from ._markdown.validator import MarkdownValidator
        return MarkdownValidator(self).validate()

    # Generate JSX from Markdown
    def render(self) -> str:
        from ..gui import Gui

        return Gui._markdown.convert(t.cast(str, self._content))


class Html(PageRenderer):
    """
    The page renderer for _HTML_ text.
    """

    def __init__(self, content: str) -> None:
        """Initializes a new `Html` page renderer.

        Args:
            content (string): The text content or the path to the file holding the HTML text to be transformed.
        """
        super().__init__(content)
        self.head = None

    # Modify path routes
    def modify_taipy_base_url(self, base_url):
        self._content = str(self._content).replace("{{taipy_base_url}}", f"/{base_url}")

    def validate(self) -> bool:
        from ._html.validator import HTMLValidator
        return HTMLValidator(self).validate()

    # Generate JSX from HTML
    def render(self) -> str:
        parser = TaipyHTMLParser()
        parser.feed(t.cast(str, self._content))
        self.head = parser.head
        return parser.get_jsx()
