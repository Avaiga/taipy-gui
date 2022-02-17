import typing as t
import warnings

from .. import PageValidator


class HTMLValidator(PageValidator):

    def validate(self) -> bool:
        return True