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
import warnings

import pytest

from taipy.gui import Gui


def test_no_ignore_file(gui: Gui):
    with warnings.catch_warnings(record=True):
        gui._set_frame(inspect.currentframe())
        gui.run(run_server=False)
        client = gui._server.test_client()
        response = client.get("/resource.txt")
        assert (
            response.status_code == 200
        ), f"file resource.txt request status should be 200 but is {response.status_code}"
