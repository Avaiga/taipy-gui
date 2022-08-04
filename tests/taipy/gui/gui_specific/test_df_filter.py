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

import numpy as np
import pandas as pd

from taipy.gui.data.utils import _df_data_filter
from taipy.gui.utils.decimator import LTTB, RDP, MinMaxDecimator


def test_data_filter_1(csvdata):
    df = _df_data_filter(csvdata[:1500], None, "Daily hospital occupancy", MinMaxDecimator(100))
    assert df.shape[0] == 100


def test_data_filter_2(csvdata):
    df = _df_data_filter(csvdata[:1500], None, "Daily hospital occupancy", LTTB(100))
    assert df.shape[0] == 100


def test_data_filter_3(csvdata):
    df = _df_data_filter(csvdata[:1500], None, "Daily hospital occupancy", RDP(n_out=100))
    assert df.shape[0] == 100


def test_data_filter_4(csvdata):
    df = _df_data_filter(csvdata[:1500], None, "Daily hospital occupancy", RDP(epsilon=100))
    assert df.shape[0] == 18
