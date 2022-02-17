import typing as t
import warnings

from .. import PageValidator


class MarkdownValidator(PageValidator):
    
    def validate(self) -> bool:
        return True