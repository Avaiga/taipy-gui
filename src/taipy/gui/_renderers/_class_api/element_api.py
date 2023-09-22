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

from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from collections.abc import Iterable

from .element_api_context_manager import _ElementApiContextManager
from .factory import _ClassApiFactory

if t.TYPE_CHECKING:
    from ...gui import Gui


class ElementApi(ABC):
    _ELEMENT_NAME = ""

    def __new__(cls, *args, **kwargs):
        obj = super(ElementApi, cls).__new__(cls)
        parent = _ElementApiContextManager().peek()
        if parent is not None:
            parent.add(obj)
        return obj

    def __init__(self, **kwargs):
        self._properties = kwargs
        self.parse_properties()

    def update(self, **kwargs):
        self._properties.update(kwargs)
        self.parse_properties()

    # Convert property value to string
    def parse_properties(self):
        self._properties = {k: ElementApi._parse_property(v) for k, v in self._properties.items()}

    @staticmethod
    def _parse_property(value: t.Any) -> t.Any:
        if isinstance(value, (str, dict, Iterable)):
            return value
        if hasattr(value, "__name__"):
            return str(getattr(value, "__name__"))
        return str(value)

    @abstractmethod
    def _render(self, gui: "Gui") -> str:
        pass


class BlockElementApi(ElementApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._children: t.List[ElementApi] = []

    def add(self, *elements: ElementApi):
        for element in elements:
            if element not in self._children:
                self._children.append(element)
        return self

    def __enter__(self):
        _ElementApiContextManager().push(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _ElementApiContextManager().pop()

    def _render(self, gui: "Gui") -> str:
        el = _ClassApiFactory.create_element(gui, self._ELEMENT_NAME, self._properties)
        return f"{el[0]}{self._render_children(gui)}</{el[1]}>"

    def _render_children(self, gui: "Gui") -> str:
        return "\n".join([child._render(gui) for child in self._children])


class DefaultBlockElement(BlockElementApi):
    _ELEMENT_NAME = "part"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ControlElementApi(ElementApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _render(self, gui: "Gui") -> str:
        el = _ClassApiFactory.create_element(gui, self._ELEMENT_NAME, self._properties)
        return (
            f"<div>{el[0]}</{el[1]}></div>"
            if f"<{el[1]}" in el[0] and f"</{el[1]}" not in el[0]
            else f"<div>{el[0]}</div>"
        )

    def __enter__(self):
        raise RuntimeError(f"Can't use context manager with control element '{self._ELEMENT_NAME}'")

    def __exit__(self, exc_type, exc_value, traceback):
        raise RuntimeError(f"Can't use context manager with control element '{self._ELEMENT_NAME}'")
