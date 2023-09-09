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

import taipy.gui.builder as tgb
from taipy.gui import Gui


def test_number_builder_1(gui: Gui, helpers):
    with tgb.Page(frame=None) as page:
        tgb.number(value="10")
    expected_list = ["<Input", 'value="10"', 'type="number"']
    helpers.test_control_builder(gui, page, expected_list)


def test_number_builder_2(gui: Gui, test_client, helpers):
    gui._bind_var_val("x", "10")
    with tgb.Page(frame=None) as page:
        tgb.number(value="{x}")
    expected_list = [
        "<Input",
        'updateVarName="_TpN_tpec_TpExPr_x_TPMDL_0"',
        'defaultValue="10"',
        'type="number"',
        "value={_TpN_tpec_TpExPr_x_TPMDL_0}",
    ]
    helpers.test_control_builder(gui, page, expected_list)
