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
from abc import ABC, abstractmethod

import numpy as np

if t.TYPE_CHECKING:
    import pandas as pd


class Decimator(ABC):
    def __init__(self, threshold: t.Optional[int], chart_zooming: t.Optional[bool]) -> None:
        """TODO: Decimator class description"""
        super().__init__()
        self.threshold = threshold
        self._chart_zooming = chart_zooming if chart_zooming is not None else True

    def _is_applicable(self, data: t.Any, nb_rows_max: int):
        if self.threshold is None:
            if nb_rows_max < len(data):
                return True
        elif self.threshold < len(data):
            return True
        return False

    @abstractmethod
    def decimate(self, data: np.ndarray, payload: t.Dict[str, t.Any]) -> np.ndarray:
        """Decimate function for decimator. This function will be executed during runtime when the appropriate conditions
        are met.
        TODO: Further explanation

        Arguments:
            data (numpy.array): A 2-dimensional array. This will be provided by taipy
            during runtime

        Returns:
            A boolean mask array for the original data
        """
        return NotImplemented


def _df_data_filter(
    dataframe: pd.DataFrame,
    x_column_name: t.Union[None, str],
    y_column_name: str,
    decimator: Decimator,
    payload: t.Dict[str, t.Any],
):
    df = dataframe.copy()
    if not x_column_name:
        index = 0
        while f"tAiPy_index_{index}" in df.columns:
            index += 1
        x_column_name = f"tAiPy_index_{index}"
        df[x_column_name] = df.index
    points = df[[x_column_name, y_column_name]].to_numpy()
    mask = decimator.decimate(points, payload)
    return df[mask]


def _df_relayout(
    dataframe: pd.DataFrame,
    x_column: t.Optional[str],
    y_column: str,
    chart_modes: t.List[str],
    x0: t.Optional[float],
    x1: t.Optional[float],
    y0: t.Optional[float],
    y1: t.Optional[float],
):
    chart_mode = chart_modes[0]
    # if chart data is invalid
    if x0 is None or x1 is None or y0 is None or y1 is None:
        return dataframe
    df = dataframe.copy()
    has_x_col = True

    if not x_column:
        index = 0
        while f"tAiPy_index_{index}" in df.columns:
            index += 1
        x_column = f"tAiPy_index_{index}"
        df[x_column] = df.index
        has_x_col = False

    # if chart_mode is empty
    if chart_mode == "lines+markers":
        # only filter by x column
        df = df.loc[(df[x_column] > x0) & (df[x_column] < x1)]
    else:
        # filter by both x and y columns
        df = df.loc[(df[x_column] > x0) & (df[x_column] < x1) & (df[y_column] > y0) & (df[y_column] < y1)]
    if not has_x_col:
        df.drop(x_column, axis=1, inplace=True)
    return df
