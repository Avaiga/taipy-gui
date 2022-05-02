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

import pandas as pd  # type: ignore

from taipy.gui import Gui


def test_expression_text_control_str(gui: Gui, helpers):
    gui._bind_var_val("x", "Hello World!")
    md_string = "<|{x}|>"
    expected_list = ["<Field", 'dataType="str"', 'defaultValue="Hello World!"', "value={x}"]
    helpers.test_control_md(gui, md_string, expected_list)


def test_expression_text_control_int(gui: Gui, helpers):
    gui._bind_var_val("x", 10)
    md_string = "<|{x}|>"
    expected_list = ["<Field", 'dataType="int"', 'defaultValue="10"', "value={x}"]
    helpers.test_control_md(gui, md_string, expected_list)


def test_expression_text_control_1(gui: Gui, helpers):
    gui._set_frame(inspect.currentframe())
    gui._bind_var_val("x", 10)
    gui._bind_var_val("y", 20)
    md_string = "<|{x + y}|>"
    expected_list = [
        "<Field",
        'dataType="int"',
        'defaultValue="30"',
        "value={tp_x_y_TPMDL_tests_DOT_taipy_DOT_gui_DOT_gui_specific_DOT_test_expression_0}",
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_expression_text_control_2(gui: Gui, helpers):
    gui._set_frame(inspect.currentframe())
    gui._bind_var_val("x", 10)
    gui._bind_var_val("y", 20)
    md_string = "<|x + y = {x + y}|>"
    expected_list = [
        "<Field",
        'dataType="str"',
        'defaultValue="x + y = 30"',
        "value={tp_x_y_x_y_TPMDL_tests_DOT_taipy_DOT_gui_DOT_gui_specific_DOT_test_expression_0}",
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_expression_text_control_3(gui: Gui, helpers):
    gui._set_frame(inspect.currentframe())
    gui._bind_var_val("x", "Mickey Mouse")
    gui._bind_var_val("y", "Donald Duck")
    md_string = "<|Hello {x} and {y}|>"
    expected_list = [
        "<Field",
        'dataType="str"',
        'defaultValue="Hello Mickey Mouse and Donald Duck"',
        "value={tp_Hello_x_and_y_TPMDL_tests_DOT_taipy_DOT_gui_DOT_gui_specific_DOT_test_expression_0}",
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_expression_text_gt_operator(gui: Gui, helpers):
    gui._set_frame(inspect.currentframe())
    gui._bind_var_val("x", 0)
    md_string = "<|{x > 0}|>"
    expected_list = [
        "<Field",
        'dataType="bool"',
        'defaultValue="false"',
        "value={tp_x_0_TPMDL_tests_DOT_taipy_DOT_gui_DOT_gui_specific_DOT_test_expression_0}",
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_expression_button_control(gui: Gui, helpers):
    gui._bind_var_val("label", "A button label")
    md_string = "<|button|label={label}|>"
    expected_list = ["<Button", 'defaultLabel="A button label"', "label={label}"]
    helpers.test_control_md(gui, md_string, expected_list)


def test_expression_table_control(gui: Gui, helpers):
    gui._set_frame(inspect.currentframe())
    gui._bind_var_val("pd", pd)
    gui._bind_var_val("series_1", pd.Series(["a", "b", "c"], name="Letters"))
    gui._bind_var_val("series_2", pd.Series([1, 2, 3], name="Numbers"))
    md_string = "<|{pd.concat([series_1, series_2], axis=1)}|table|page_size=10|columns=Letters;Numbers|>"
    expected_list = [
        "<Table",
        'columns="{&quot;Letters&quot;: &#x7B;&quot;index&quot;: 0, &quot;type&quot;: &quot;object&quot;, &quot;dfid&quot;: &quot;Letters&quot;&#x7D;, &quot;Numbers&quot;: &#x7B;&quot;index&quot;: 1, &quot;type&quot;: &quot;int&quot;, &quot;dfid&quot;: &quot;Numbers&quot;&#x7D;}"',
        'updateVarName="_TpD_tp_pd_concat_series_1_series_2_axis_1_TPMDL_tests_DOT_taipy_DOT_gui_DOT_gui_specific_DOT_test_expression_0"',
        "data={_TpD_tp_pd_concat_series_1_series_2_axis_1_TPMDL_tests_DOT_taipy_DOT_gui_DOT_gui_specific_DOT_test_expression_0}",
    ]
    helpers.test_control_md(gui, md_string, expected_list)
    assert isinstance(
        gui._bindings()
        ._get_data_scope()
        ._TpD_tp_pd_concat_series_1_series_2_axis_1_TPMDL_tests_DOT_taipy_DOT_gui_DOT_gui_specific_DOT_test_expression_0.get(),
        pd.DataFrame,
    )


def test_lambda_expression_selector(gui: Gui, helpers):
    gui._bind_var_val(
        "lov",
        [
            {"id": "1", "name": "scenario 1"},
            {"id": "3", "name": "scenario 3"},
            {"id": "2", "name": "scenario 2"},
        ],
    )
    gui._bind_var_val("sel", {"id": "1", "name": "scenario 1"})
    md_string = "<|{sel}|selector|lov={lov}|type=test|adapter={lambda elt: (elt['id'], elt['name'])}|>"
    expected_list = [
        "<Selector",
        'defaultLov="[[&quot;1&quot;, &quot;scenario 1&quot;], [&quot;3&quot;, &quot;scenario 3&quot;], [&quot;2&quot;, &quot;scenario 2&quot;]]"',
        'defaultValue="[&quot;1&quot;]"',
        'updateVars="lov=_TpL_lov"',
        "lov={_TpL_lov}",
        'updateVarName="_TpLv_sel"',
        "value={_TpLv_sel}",
    ]
    helpers.test_control_md(gui, md_string, expected_list)
