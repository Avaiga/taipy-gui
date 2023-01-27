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

import inspect

from taipy.gui import Gui


def test_status_md(gui: Gui, helpers):
    status = [{"status": "info", "message": "Info Message"}]  # noqa: F841
    md_string = "<|{status}|status|>"
    expected_list = [
        "<Status",
        'defaultValue="[&#x7B;&quot;status&quot;: &quot;info&quot;, &quot;message&quot;: &quot;Info Message&quot;&#x7D;]"',
        "value={tpec_TpExPr_status_TPMDL_0}",
    ]
    gui._set_frame(inspect.currentframe())
    helpers.test_control_md(gui, md_string, expected_list)


def test_status_html(gui: Gui, helpers):
    status = [{"status": "info", "message": "Info Message"}]  # noqa: F841
    html_string = '<taipy:status value="{status}" />'
    expected_list = [
        "<Status",
        'defaultValue="[&#x7B;&quot;status&quot;: &quot;info&quot;, &quot;message&quot;: &quot;Info Message&quot;&#x7D;]"',
        "value={tpec_TpExPr_status_TPMDL_0}",
    ]
    gui._set_frame(inspect.currentframe())
    helpers.test_control_html(gui, html_string, expected_list)
