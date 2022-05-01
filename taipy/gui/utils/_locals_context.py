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

import typing as t


class _LocalsContext:
    def __init__(self) -> None:
        self.__default_module: str = ""
        self._locals_map: t.Dict[str, t.Dict[str, t.Any]] = {}
        self.__current_context: t.Optional[str] = None

    def set_default(self, default: t.Dict[str, t.Any]) -> None:
        self.__default_module = default.get("__name__", "")
        self._locals_map[self.__default_module] = default

    def get_default(self) -> t.Dict[str, t.Any]:
        return self._locals_map[self.__default_module]

    def get_all_keys(self) -> t.Set[str]:
        keys = set()
        for _, v in self._locals_map.items():
            for i in v.keys():
                keys.add(i)
        return keys

    def add(self, context: t.Optional[str], locals_dict: t.Optional[t.Dict[str, t.Any]]):
        if context is not None and locals_dict is not None and context not in self._locals_map:
            self._locals_map[context] = locals_dict

    def set_locals_context(self, context: t.Optional[str]) -> None:
        if context in self._locals_map:
            self.__current_context = context

    def get_locals(self) -> t.Dict[str, t.Any]:
        return self.get_default() if (context := self.get_context()) is None else self._locals_map[context]

    def get_context(self) -> t.Optional[str]:
        return self.__current_context

    def is_default(self) -> bool:
        return self.get_default == self.get_locals()

    def reset_locals_context(self) -> None:
        self.__current_context = None
