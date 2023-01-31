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
import warnings
from abc import ABC, abstractmethod

import numpy as np

if t.TYPE_CHECKING:
    import pandas as pd


class Decimator(ABC):
    """Decimator provides a way to reduce the number of data being displayed in charts
    while retaining the overall shape of the charts. This is a base class that could be
    extended by the user. taipy-gui comes out-of-the-box with several implementation of
    this class for different use cases.
    """

    _CHART_MODES: t.List[str] = []

    def __init__(self, threshold: t.Optional[int], zoom: t.Optional[bool]) -> None:
        """Initialize a new Decimator.

        Arguments:
            threshold (Optional[int]): The minimum amount of data points before the
                decimator class can be applied
            zoom (Optional[bool]): set to True if you want to reapply the decimator class
                whenever a zoom/relayout event is triggered
        """
        super().__init__()
        self.threshold = threshold
        self._zoom = zoom if zoom is not None else True

    def _is_applicable(self, data: t.Any, nb_rows_max: int, chart_mode: str):
        if chart_mode not in self._CHART_MODES:
            warnings.warn(f"{type(self).__name__} is only applicable for {' '.join(self._CHART_MODES)}")
            return False
        if self.threshold is None:
            if nb_rows_max < len(data):
                return True
        elif self.threshold < len(data):
            return True
        return False

    @abstractmethod
    def decimate(self, data: np.ndarray, payload: t.Dict[str, t.Any]) -> np.ndarray:
        """Decimate function for decimator.

        This function is executed when the appropriate conditions are met. This function holds
        the algorithm to determines which data points will be kept or removed.

        Arguments:
            data (numpy.array): A 2D or 3D numpy array.
            payload (Dict[str, any]): additional information on charts that will be provided
                during runtime

        Returns:
            A boolean mask array for the original data. Return True to keep the row, False
            to remove the row.
        """
        return NotImplementedError  # type: ignore


def _df_data_filter(
    dataframe: pd.DataFrame,
    x_column_name: t.Optional[str],
    y_column_name: str,
    z_column_name: str,
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
    column_list = [x_column_name, y_column_name, z_column_name] if z_column_name else [x_column_name, y_column_name]
    points = df[column_list].to_numpy()
    mask = decimator.decimate(points, payload)
    return df[mask]


def _df_relayout(
    dataframe: pd.DataFrame,
    x_column: t.Optional[str],
    y_column: str,
    chart_mode: str,
    x0: t.Optional[float],
    x1: t.Optional[float],
    y0: t.Optional[float],
    y1: t.Optional[float],
):
    if chart_mode not in ["lines+markers", "markers"]:
        return dataframe
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
        df = df.loc[(df[x_column] > x0) & (df[x_column] < x1) & (df[y_column] > y0) & (df[y_column] < y1)]  # noqa
    if not has_x_col:
        df.drop(x_column, axis=1, inplace=True)
    return df
