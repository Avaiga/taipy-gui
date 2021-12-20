import pytest

from taipy.config._config import _Config
from taipy.config.config import Config


@pytest.fixture(scope="function", autouse=True)
def reset_configuration_singleton():
    yield
    Config._python_config = _Config()
    Config._file_config = _Config()
    Config._env_config = _Config()
    Config._applied_config = _Config.default_config()


task1_config = Config.add_task("task1", [], print, [])
task2_config = Config.add_task("task2", [], print, [])


def test_pipeline_config_creation():
    pipeline_config = Config.add_pipeline("pipelines1", [task1_config, task2_config])

    assert list(Config.pipelines()) == ["default", pipeline_config.name]

    pipeline2_config = Config.add_pipeline("pipelines2", [task1_config, task2_config])
    assert list(Config.pipelines()) == ["default", pipeline_config.name, pipeline2_config.name]


def test_pipeline_count():
    Config.add_pipeline("pipelines1", [task1_config, task2_config])
    assert len(Config.pipelines()) == 2

    Config.add_pipeline("pipelines2", [task1_config, task2_config])
    assert len(Config.pipelines()) == 3

    Config.add_pipeline("pipelines3", [task1_config, task2_config])
    assert len(Config.pipelines()) == 4


def test_pipeline_getitem():
    pipeline_config_name = "pipelines1"
    pipeline = Config.add_pipeline(pipeline_config_name, [task1_config, task2_config])

    assert Config.pipelines()[pipeline_config_name].name == pipeline.name
    assert Config.pipelines()[pipeline_config_name].tasks == pipeline.tasks
    assert Config.pipelines()[pipeline_config_name].properties == pipeline.properties


def test_pipeline_creation_no_duplication():
    Config.add_pipeline("pipelines1", [task1_config, task2_config])

    assert len(Config.pipelines()) == 2

    Config.add_pipeline("pipelines1", [task1_config, task2_config])
    assert len(Config.pipelines()) == 2
