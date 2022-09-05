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

import warnings
from datetime import date, datetime, time
from pathlib import Path

from flask.json.provider import DefaultJSONProvider

from ..icon import Icon
from ..utils import _date_to_ISO, _MapDict, _TaipyBase


class _TaipyJsonProvider(DefaultJSONProvider):
    @staticmethod
    def default(o):
        if isinstance(o, Icon):
            return o._to_dict()
        elif isinstance(o, _MapDict):
            return o._dict
        elif isinstance(o, _TaipyBase):
            return o.get()
        elif isinstance(o, (datetime, date, time)):
            return _date_to_ISO(o)
        elif isinstance(o, Path):
            return str(o)
        warnings.warn(f"Object of type {type(o).__name__} is not JSON serializable")
