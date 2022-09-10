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

import numpy as np

from ..utils import Decimator


class ScatterDecimator(Decimator):
    def __init__(
        self,
        applied_threshold: t.Optional[int] = None,
        chart_zooming: t.Optional[bool] = True,
    ):
        super().__init__(applied_threshold, chart_zooming)

    def decimate(self, data: np.ndarray, payload: t.Any) -> np.ndarray:
        pass
