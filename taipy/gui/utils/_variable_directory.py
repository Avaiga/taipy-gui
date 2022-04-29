# Copyright 2022 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import re
import typing as t
from types import FrameType

from ._locals_context import _LocalsContext
from .get_imported_var import _get_imported_var
from .get_module_name import _get_module_name_from_frame, _get_module_name_from_imported_var


class _VariableDirectory:
    def __init__(self, locals_context: _LocalsContext):
        self._locals_context = locals_context
        self._default_module = ""
        self._var_dir: dict[str, dict] = {}
        self._linked_var_dir: dict[str, dict] = {}
        self._imported_var_dir: dict[str, list[tuple[str, str, str]]] = {}

    def set_default(self, frame: FrameType) -> None:
        self._default_module = _get_module_name_from_frame(frame)
        self.add_frame(frame)

    def add_frame(self, frame: t.Optional[FrameType]) -> None:
        if frame is None:
            return
        module_name = _get_module_name_from_frame(frame)
        if module_name not in self._imported_var_dir:
            imported_var_list = _get_imported_var(frame)
            self._imported_var_dir[module_name] = imported_var_list

    def process_imported_var(self) -> None:
        default_imported_dir = self._imported_var_dir[self._default_module]
        self._locals_context.set_locals_context(self._default_module)
        for name, asname, module in default_imported_dir:
            imported_module_name = _get_module_name_from_imported_var(
                name, self._locals_context.get_locals()[asname], module
            )
            print(imported_module_name)
        self._locals_context.reset_locals_context()

        for k, v in self._imported_var_dir.items():
            self._locals_context.set_locals_context(k)
            for name, asname, module in v:
                imported_module_name = _get_module_name_from_imported_var(
                    name, self._locals_context.get_locals()[asname], module
                )
                print(imported_module_name)
            self._locals_context.reset_locals_context()

    def add_var(self, name, module) -> str:
        var_name = _variable_encode(name, module) if module != self._default_module else name
        if name not in self._var_dir:
            self._var_dir[name] = {module: var_name}
        else:
            self._var_dir[name][module] = var_name
        return var_name


def _variable_encode(var_name: str, module_name: t.Optional[str]):
    if module_name is None:
        return var_name
    module_name = module_name.replace(".", "_DOT_")
    return f"{var_name}_TPMDL_{module_name}"


def _variable_decode(var_name: str):
    if result := re.compile(r"(.*?)_TPMDL_(.*)").match(var_name):
        return result[1], result[2].replace("_DOT_", ".")
    return var_name, None
