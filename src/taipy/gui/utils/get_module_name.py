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

import inspect
import sys
import typing as t
from types import FrameType, ModuleType


def _get_module_name_from_frame(frame: FrameType):
    return frame.f_globals["__name__"] if "__name__" in frame.f_globals else None


def _get_module_name_from_imported_var(var_name: str, value: t.Any, sub_module_name: str) -> str:
    module_list = sys.modules.copy()
    # the provided sub_module_name are expected to contain only part of the full module_name provided by sys.modules
    # --> we can find potential matched modules based on the sub_module_name
    potential_matched_module = [m for m in module_list.keys() if m.endswith(sub_module_name)]
    for m in potential_matched_module:
        module = module_list[m]
        if hasattr(module, var_name) and getattr(module, var_name) is value:
            return m
    # failed fetching any matched module with variable and value
    return sub_module_name
