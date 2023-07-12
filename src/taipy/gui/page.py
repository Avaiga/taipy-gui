# Copyright 2023 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import inspect
import typing as t
from abc import ABC, abstractmethod
from os import path
from types import FrameType

from .utils import _filter_locals, _get_module_name_from_frame, _is_in_notebook, _varname_from_content


class Page(ABC):
    """Generic page generator.

    The `Page` class transforms template text into actual pages that can be displayed
    on a web browser.

    When a page is requested to be displayed, it is converted into HTML
    code that can be sent to the client. All control placeholders are
    replaced by their respective graphical component so you can show
    your application variables and interact with them.
    """

    def __init__(self, content: str, **kwargs) -> None:
        """Initialize a new Page with the indicated content.

        Arguments:
            content (str): The text content or the path to the file holding the text to be transformed.

        If *content* is a path to a readable file, the file is read entirely as the text template.
        """
        self._content = ""
        self._filepath = ""
        self._class_module_name = ""
        self._class_locals: t.Dict[str, t.Any] = {}
        self._frame: t.Optional[FrameType] = None
        if "frame" in kwargs:
            self._frame = kwargs.get("frame")
        else:
            # Get the correct frame from Markdown, Html class by going back 2 stacks
            self._frame = t.cast(FrameType, t.cast(FrameType, inspect.stack()[2].frame))
        self.__process_content(content)

    def __process_content(self, content: str) -> None:
        if path.exists(content) and path.isfile(content):
            return self.__parse_file_content(content)
        if self._frame is not None:
            frame_dir_path = path.dirname(path.abspath(self._frame.f_code.co_filename))
            content_path = path.join(frame_dir_path, content)
            if path.exists(content_path) and path.isfile(content_path):
                return self.__parse_file_content(content_path)
        self._content = content

    def __parse_file_content(self, content):
        with open(t.cast(str, content), "r") as f:
            self._content = f.read()
            # Save file path for error handling
            self._filepath = content

    def set_content(self, content: str) -> None:
        """Set a new page content.

        Reads the new page content and reinitializes the page to reflect the change.

        !!! important
            This function can only be used an IPython notebook context.

        Arguments:
            content (str): The text content or the path to the file holding the text to be transformed.
                If *content* is a path to a readable file, the file is read entirely as the text
                template.

        Exceptions:
            RuntimeError: If this method is called outside an IPython notebook context.
        """
        if not _is_in_notebook():
            raise RuntimeError("'set_content()' must be used in an IPython notebook context")
        self.__process_content(content)

    def _get_content_detail(self, gui) -> str:
        if self._filepath:
            return f"in file '{self._filepath}'"
        if varname := _varname_from_content(gui, self._content):
            return f"in variable '{varname}'"
        return ""

    def _get_locals(self) -> t.Optional[t.Dict[str, t.Any]]:
        return (
            self._class_locals
            if self._is_class_module()
            else None
            if self._frame is None
            else _filter_locals(self._frame.f_locals)
        )

    def _set_class_module(self, name: str, locals_: t.Dict[str, t.Any]) -> None:
        self._class_module_name = name
        self._class_locals = locals_

    def _is_class_module(self):
        return self._class_module_name != ""

    def _get_module_name(self) -> t.Optional[str]:
        return (
            None
            if self._frame is None
            else f"{_get_module_name_from_frame(self._frame)}{'.' if self._class_module_name else ''}{self._class_module_name}"
        )

    @abstractmethod
    def render(self, gui) -> str:
        pass
