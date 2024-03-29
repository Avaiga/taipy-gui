# Copyright 2021-2024 Avaiga Private Limited
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import pytest


def pytest_addoption(parser):
    parser.addoption("--e2e-base-url", action="store", default="/", help="base url for e2e testing")
    parser.addoption("--e2e-port", action="store", default="5000", help="port for e2e testing")


@pytest.fixture(scope="session")
def e2e_base_url(request):
    return request.config.getoption("--e2e-base-url")


@pytest.fixture(scope="session")
def e2e_port(request):
    return request.config.getoption("--e2e-port")
