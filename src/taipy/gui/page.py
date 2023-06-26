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
from types import FrameType

from .utils import _filter_locals, _get_module_name_from_frame

if t.TYPE_CHECKING:
    from .renderers import _Renderer


class Page:
    """Generic page generator.

    The `Page` class transforms template text into actual pages that can be displayed
    on a web browser.

    When a page is requested to be displayed, it is converted into HTML
    code that can be sent to the client. All control placeholders are
    replaced by their respective graphical component so you can show
    your application variables and interact with them.
    """

    def __init__(self, **kwargs) -> None:
        is_class_module = kwargs.get("is_class_module", False)
        self._class_module_name = ""
        self._class_locals: t.Dict[str, t.Any] = {}
        self._frame: t.Optional[FrameType] = None
        self._renderer: t.Optional["_Renderer"] = getattr(self, "renderer", None)
        if "frame" in kwargs:
            self._frame = kwargs.get("frame")
        else:
            if is_class_module:
                if self._renderer is None:
                    raise AttributeError(f"Page '{type(self).__name__}' must have a 'renderer' attribute")
                self._frame = self._renderer._frame
            else:
                if len(inspect.stack()) < 4:
                    raise RuntimeError(f"Can't resolve module. Page '{type(self).__name__}' is not registered.")
                self._frame = t.cast(FrameType, t.cast(FrameType, inspect.stack()[3].frame))
        self.__extract_page_class(is_class_module)

    def register_page(self) -> None:
        Page.__init__(self, is_class_module=True)

    def __extract_page_class(self, is_class_module: bool = False):
        if not is_class_module:
            return
        cls = type(self)
        valid_func = [
            i[0]
            for i in inspect.getmembers(cls)
            if not i[0].startswith("_") and (inspect.ismethod(i[1]) or inspect.isfunction(i[1]))
        ]
        cls_locals = dict(self.__dict__.items())
        for f in valid_func:
            cls_locals[f] = getattr(self, f).__func__
        self._set_class_module(cls.__name__, cls_locals)

    def _get_locals(self) -> t.Optional[t.Dict[str, t.Any]]:
        return (
            self._class_locals
            if self._is_class_module()
            else None
            if (frame := self._get_frame()) is None
            else _filter_locals(frame.f_locals)
        )

    def _set_class_module(self, name: str, locals_: t.Dict[str, t.Any]) -> None:
        self._class_module_name = name
        self._class_locals = locals_

    def _is_class_module(self):
        return self._class_module_name != ""

    def _get_frame(self):
        if not hasattr(self, "_frame"):
            raise RuntimeError(f"Page '{type(self).__name__}' was not registered correctly.")
        return self._frame

    def _get_module_name(self) -> t.Optional[str]:
        return (
            None
            if (frame := self._get_frame()) is None
            else f"{_get_module_name_from_frame(frame)}{'.' if self._class_module_name else ''}{self._class_module_name}"
        )

    def _get_content_detail(self, gui) -> str:
        return f"in class {type(self).__name__}"

    def render(self, gui) -> str:
        if self._renderer is not None:
            return self._renderer.render(gui)
        return "<h1>No renderer found for page</h1>"
