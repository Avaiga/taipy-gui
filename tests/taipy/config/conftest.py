import copy
import os

import pytest

from taipy.config._config import _Config
from taipy.config.config import Config


@pytest.fixture(scope="function", autouse=True)
def reset_configuration_singleton():
    _env = copy.deepcopy(os.environ)
    yield
    Config._python_config = _Config()
    Config._file_config = None
    Config._env_config = None
    Config._applied_config = _Config.default_config()

    os.environ = _env
