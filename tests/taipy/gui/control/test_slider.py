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

from taipy.gui import Gui


def test_slider_md(gui: Gui, test_client, helpers):
    gui._bind_var_val("x", 10)
    md_string = "<|{x}|slider|>"
    expected_list = [
        "<Slider",
        'updateVarName="_TpN_tpec_TpExPr_x_TPMDL_0',
        "defaultValue={10}",
        "value={_TpN_tpec_TpExPr_x_TPMDL_0}",
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_slider_with_min_max(gui: Gui, test_client, helpers):
    gui._bind_var_val("x", 0)
    md_string = "<|{x}|slider|min=-10|max=10|>"
    expected_list = ["<Slider", "min={-10.0}", "max={10.0}", "defaultValue={0}"]
    helpers.test_control_md(gui, md_string, expected_list)


def test_slider_items_md(gui: Gui, test_client, helpers):
    gui._bind_var_val("x", "Item 1")
    md_string = "<|{x}|slider|lov=Item 1;Item 2;Item 3|text_anchor=left|>"
    expected_list = [
        "<Slider",
        'updateVarName="_TpLv_tpec_TpExPr_x_TPMDL_0"',
        "value={_TpLv_tpec_TpExPr_x_TPMDL_0}",
        'defaultLov="[&quot;Item 1&quot;, &quot;Item 2&quot;, &quot;Item 3&quot;]"',
        'defaultValue="[&quot;Item 1&quot;]"',
        'textAnchor="left"',
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_slider_text_anchor_md(gui: Gui, test_client, helpers):
    gui._bind_var_val("x", "Item 1")
    md_string = "<|{x}|slider|text_anchor=NoNe|>"
    expected_list = [
        "<Slider",
        'updateVarName="_TpN_tpec_TpExPr_x_TPMDL_0"',
        "value={_TpN_tpec_TpExPr_x_TPMDL_0}",
        'textAnchor="none"',
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_slider_text_anchor_default_md(gui: Gui, test_client, helpers):
    gui._bind_var_val("x", "Item 1")
    md_string = "<|{x}|slider|items=Item 1|>"
    expected_list = [
        "<Slider",
        'updateVarName="_TpN_tpec_TpExPr_x_TPMDL_0"',
        "value={_TpN_tpec_TpExPr_x_TPMDL_0}",
        'textAnchor="bottom"',
    ]
    helpers.test_control_md(gui, md_string, expected_list)


def test_slider_html_1(gui: Gui, test_client, helpers):
    gui._bind_var_val("x", 10)
    html_string = '<taipy:slider value="{x}" />'
    expected_list = [
        "<Slider",
        'updateVarName="_TpN_tpec_TpExPr_x_TPMDL_0"',
        "defaultValue={10}",
        "value={_TpN_tpec_TpExPr_x_TPMDL_0}",
    ]
    helpers.test_control_html(gui, html_string, expected_list)


def test_slider_html_2(gui: Gui, test_client, helpers):
    gui._bind_var_val("x", 10)
    html_string = "<taipy:slider>{x}</taipy:slider>"
    expected_list = [
        "<Slider",
        'updateVarName="_TpN_tpec_TpExPr_x_TPMDL_0"',
        "defaultValue={10}",
        "value={_TpN_tpec_TpExPr_x_TPMDL_0}",
    ]
    helpers.test_control_html(gui, html_string, expected_list)
