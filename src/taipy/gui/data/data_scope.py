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

from __future__ import annotations

import typing as t
import warnings
from types import SimpleNamespace


class _DataScopes:

    _GLOBAL_ID = "global"

    def __init__(self) -> None:
        self.__scopes: t.Dict[str, SimpleNamespace] = {_DataScopes._GLOBAL_ID: SimpleNamespace()}
        self.__single_client = True

    def set_single_client(self, value: bool) -> None:
        self.__single_client = value

    def get_single_client(self) -> bool:
        return self.__single_client

    def get_scope(self, client_id: t.Optional[str]) -> SimpleNamespace:
        if self.__single_client:
            return self.__scopes[_DataScopes._GLOBAL_ID]
        # global context in case request is not registered or client_id is not available (such as in the context of running tests)
        if not client_id:
            warnings.warn("Empty session id, using global scope instead")
            return self.__scopes[_DataScopes._GLOBAL_ID]
        if client_id not in self.__scopes:
            warnings.warn(
                f"session id {client_id} not found in data scope. Taipy will automatically create a scope for this session id but you might have to reload your webpage"
            )
            self.create_scope(client_id)
        return self.__scopes[client_id]

    def get_all_scopes(self) -> t.Dict[str, SimpleNamespace]:
        return self.__scopes

    def broadcast_data(self, name, value):
        if self.__single_client:
            return
        if not self.__client_id:
            for _, v in self.__scopes.items():
                if hasattr(v, name):
                    setattr(v, name, value)

    def create_scope(self, id: str) -> None:
        if self.__single_client:
            return
        if id is None:
            warnings.warn("Empty session id, might be due to unestablished WebSocket connection")
            return
        if id not in self.__scopes:
            self.__scopes[id] = SimpleNamespace()

    def delete_scope(self, id: str) -> None:  # pragma: no cover
        if self.__single_client:
            return
        if id is None:
            warnings.warn("Empty session id, might be due to unestablished WebSocket connection")
            return
        if id in self.__scopes:
            del self.__scopes[id]
