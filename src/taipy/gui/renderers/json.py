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
from json import JSONEncoder
from pathlib import Path

from flask.json.provider import DefaultJSONProvider

from ..icon import Icon
from ..utils import _date_to_ISO, _MapDict, _TaipyBase


def _default(o):
    if isinstance(o, Icon):
        return o._to_dict()
    if isinstance(o, _MapDict):
        return o._dict
    if isinstance(o, _TaipyBase):
        return o.get()
    if isinstance(o, (datetime, date, time)):
        return _date_to_ISO(o)
    if isinstance(o, Path):
        return str(o)
    try:
        raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
    except Exception as e:
        warnings.warn(f"JSONEncoder has thrown {e}")
        return None


class _TaipyJsonEncoder(JSONEncoder):
    def default(self, o):
        return _default(o)


class _TaipyJsonProvider(DefaultJSONProvider):
    default = staticmethod(_default)  # type: ignore
