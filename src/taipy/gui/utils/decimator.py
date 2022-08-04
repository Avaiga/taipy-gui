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
from abc import ABC, abstractmethod

import numpy as np


class Decimator(ABC):
    def __init__(self, applied_threshold: t.Optional[int]) -> None:
        self.applied_threshold = applied_threshold
        super().__init__()

    def _is_applicable(self, data: t.Any, nb_rows_max: int):
        if self.applied_threshold is None:
            if nb_rows_max < len(data):
                return True
        elif self.applied_threshold < len(data):
            return True
        return False

    @abstractmethod
    def decimate(self, data: np.ndarray) -> np.ndarray:
        """Decimate function for decimator
        Arguments:
            data (numpy.array): A 2-dimensional array. This will be provided by taipy
            during runtime

        Returns:
            A boolean mask array for the original data
        """
        return NotImplemented


class RDP(Decimator):
    def __init__(self, epsilon: int, applied_threshold: t.Optional[int] = None):
        super().__init__(applied_threshold)
        self._epsilon = epsilon

    @staticmethod
    def dsquared_line_points(P1, P2, points):
        """
        Calculate only squared distance, only needed for comparison
        """
        xdiff = P2[0] - P1[0]
        ydiff = P2[1] - P1[1]
        nom = (ydiff * points[:, 0] - xdiff * points[:, 1] + P2[0] * P1[1] - P2[1] * P1[0]) ** 2
        denom = ydiff**2 + xdiff**2
        return np.divide(nom, denom)

    def decimate(self, data: np.ndarray) -> np.ndarray:
        # initiate mask array
        # same amount of points
        mask = np.empty(data.shape[0], dtype=bool)

        # Assume all points are valid and falsify those which are found
        mask.fill(True)

        # The stack to select start and end index
        stack = [(0, data.shape[0] - 1)]

        while stack:
            # Pop the last item
            (start, end) = stack.pop()

            # nothing to calculate if no points in between
            if end - start <= 1:
                continue

            # Calculate distance to points
            P1 = data[start]
            P2 = data[end]
            points = data[start + 1 : end]
            dsq = RDP.dsquared_line_points(P1, P2, points)

            mask_eps = dsq > self._epsilon**2

            if mask_eps.any():
                # max point outside eps
                # Include index that was sliced out
                # Also include the start index to get absolute index
                # And not relative
                mid = np.argmax(dsq) + 1 + start
                stack.append((start, mid))
                stack.append((mid, end))

            else:
                # Points in between are redundant
                mask[start + 1 : end] = False

        return mask


class MinMaxDecimator(Decimator):
    def __init__(self, n_out: int, applied_threshold: t.Optional[int] = None):
        super().__init__(applied_threshold)
        self._n_out = n_out

    def decimate(self, data: np.ndarray) -> np.ndarray:
        if self._n_out >= data.shape[0]:
            return np.full(len(data), False)
        # Create a boolean mask
        x = data[:, 0]
        y = data[:, 1]
        num_bins = self._n_out
        pts_per_bin = x.size // num_bins
        # Create temp to hold the reshaped & slightly cropped y
        y_temp = y[: num_bins * pts_per_bin].reshape((num_bins, pts_per_bin))
        # use argmax/min to get column locations
        cc_max = np.argmax(y_temp, axis=1)
        cc_min = np.argmin(y_temp, axis=1)
        rr = np.arange(0, num_bins)
        # compute the flat index to where these are
        flat_max = cc_max + rr * pts_per_bin
        flat_min = cc_min + rr * pts_per_bin
        mm_mask = np.full((x.size,), False)
        mm_mask[flat_max] = True
        mm_mask[flat_min] = True
        return mm_mask


class LTTB(Decimator):
    def __init__(self, n_out: int, applied_threshold: t.Optional[int] = None) -> None:
        super().__init__(applied_threshold)
        self._n_out = n_out

    @staticmethod
    def _areas_of_triangles(a, bs, c):
        bs_minus_a = bs - a
        a_minus_bs = a - bs
        return 0.5 * abs((a[0] - c[0]) * (bs_minus_a[:, 1]) - (a_minus_bs[:, 0]) * (c[1] - a[1]))

    def decimate(self, data: np.ndarray) -> np.ndarray:
        n_out = self._n_out
        if n_out >= data.shape[0]:
            return np.full(len(data), True)

        if n_out < 3:
            raise ValueError("Can only downsample to a minimum of 3 points")

        # Split data into bins
        n_bins = n_out - 2
        data_bins = np.array_split(data[1:-1], n_bins)

        prev_a = data[0]
        start_pos = 0

        # Prepare output mask array
        # First and last points are the same as in the input.
        out_mask = np.full(len(data), False)
        out_mask[0] = True
        out_mask[len(data) - 1] = True

        # Largest Triangle Three Buckets (LTTB):
        # In each bin, find the point that makes the largest triangle
        # with the point saved in the previous bin
        # and the centroid of the points in the next bin.
        for i in range(len(data_bins)):
            this_bin = data_bins[i]
            next_bin = data_bins[i + 1] if i < n_bins - 1 else data[-1:]
            a = prev_a
            bs = this_bin
            c = next_bin.mean(axis=0)

            areas = LTTB._areas_of_triangles(a, bs, c)
            bs_pos = np.argmax(areas)
            prev_a = bs[bs_pos]
            out_mask[start_pos + bs_pos] = True
            start_pos += len(this_bin)

        return out_mask
