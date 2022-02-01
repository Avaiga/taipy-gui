__all__ = ["Config"]

import logging
import os
from typing import Callable, Dict, List, Optional, Union

from taipy.common.frequency import Frequency
from taipy.config._config import _Config
from taipy.config.checker.checker import Checker
from taipy.config.checker.issue_collector import IssueCollector
from taipy.config.data_node_config import DataNodeConfig
from taipy.config.global_app import GlobalAppConfig
from taipy.config.job_config import JobConfig
from taipy.config.pipeline_config import PipelineConfig
from taipy.config.scenario_config import ScenarioConfig
from taipy.config.task_config import TaskConfig
from taipy.config.toml_serializer import TomlSerializer
from taipy.data.scope import Scope
from taipy.exceptions.configuration import ConfigurationIssueError


class Config:
    """Singleton entry point to configure Taipy application and retrieve the configuration values."""

    ENVIRONMENT_VARIABLE_NAME_WITH_CONFIG_PATH = "TAIPY_CONFIG_PATH"
    _python_config = _Config()
    _file_config = None
    _env_file_config = None
    _applied_config = _Config.default_config()
    collector = IssueCollector()

    @classmethod
    def global_config(cls) -> GlobalAppConfig:
        """Returns configuration values related to the global application."""
        return cls._applied_config.global_config

    @classmethod
    def job_config(cls) -> JobConfig:
        """Returns configuration values related to the job executions."""
        return cls._applied_config.job_config

    @classmethod
    def data_nodes(cls) -> Dict[str, DataNodeConfig]:
        """Returns data node configs by config name."""
        return cls._applied_config.data_nodes

    @classmethod
    def tasks(cls) -> Dict[str, TaskConfig]:
        """Returns task configs by config name."""
        return cls._applied_config.tasks

    @classmethod
    def pipelines(cls) -> Dict[str, PipelineConfig]:
        """Returns pipeline configs by config name."""
        return cls._applied_config.pipelines

    @classmethod
    def scenarios(cls) -> Dict[str, ScenarioConfig]:
        """Returns scenario configs by config name."""
        return cls._applied_config.scenarios

    @classmethod
    def load(cls, filename):
        """
        Loads configuration from file located at the filename given as parameter.

        Parameters:
            filename (str or Path): File to load.
        """
        logging.info(f"Loading configuration filename '{filename}'")
        cls._file_config = TomlSerializer().read(filename)
        logging.info(f"Successful loaded configuration filename '{filename}'")
        cls.__compile_configs()

    @classmethod
    def export(cls, filename):
        """
        Exports the configuration to a toml file.

        The configuration exported is the configuration applied. It is compiled from the three possible methods to
        configure the application: The python code configuration, the file configuration and the environment
        configuration.

        Parameters:
            filename (str or Path): File to export.
        Note:
            Overwrite the file if it already exists.
        """
        TomlSerializer().write(cls._applied_config, filename)

    @classmethod
    def export_code_config(cls, filename):
        """
        Exports the python code configuration as a toml file.

        Parameters:
            filename (str): File to export.
        Note:
            Overwrite the file if it already exists.
        """
        TomlSerializer().write(cls._python_config, filename)

    @classmethod
    def set_global_config(
        cls,
        notification: Union[bool, str] = None,
        broker_endpoint: str = None,
        root_folder: str = None,
        storage_folder: str = None,
        **properties,
    ):
        """Configures fields related to global application."""
        cls._python_config.global_config = GlobalAppConfig(
            notification, broker_endpoint, root_folder, storage_folder, **properties
        )
        cls.__compile_configs()
        return cls._applied_config.global_config

    @classmethod
    def set_job_config(
        cls,
        mode: str = None,
        nb_of_workers: Union[int, str] = None,
        hostname: str = None,
        airflow_dags_folder: str = None,
        airflow_folder: str = None,
        airflow_db_endpoint: str = None,
        start_airflow: Union[bool, str] = None,
        airflow_api_retry: Union[int, str] = None,
        **properties,
    ):
        """Configures fields related to job execution."""
        job_config = JobConfig(
            mode,
            nb_of_workers,
            hostname,
            airflow_dags_folder,
            airflow_folder,
            airflow_db_endpoint,
            start_airflow,
            airflow_api_retry,
            **properties,
        )
        cls._python_config.job_config = job_config
        cls.__compile_configs()
        return cls._applied_config.job_config

    @classmethod
    def add_data_node(
        cls,
        name: str,
        storage_type: str = DataNodeConfig.DEFAULT_STORAGE_TYPE,
        scope: Scope = DataNodeConfig.DEFAULT_SCOPE,
        **properties,
    ):
        """Adds a new data node configuration."""
        ds_config = DataNodeConfig(name, storage_type, scope, **properties)
        cls._python_config.data_nodes[ds_config.name] = ds_config
        cls.__compile_configs()
        return cls._applied_config.data_nodes[ds_config.name]

    @classmethod
    def add_default_data_node(cls, storage_type: str, scope=Scope.PIPELINE, **properties):
        """Configures the default data node configuration."""
        data_node_config = DataNodeConfig(_Config.DEFAULT_KEY, storage_type, scope, **properties)
        cls._python_config.data_nodes[_Config.DEFAULT_KEY] = data_node_config
        cls.__compile_configs()
        return cls._applied_config.data_nodes[_Config.DEFAULT_KEY]

    @classmethod
    def add_task(
        cls,
        name: str,
        input: Union[DataNodeConfig, List[DataNodeConfig]],
        function,
        output: Union[DataNodeConfig, List[DataNodeConfig]],
        **properties,
    ):
        """Adds a new task configuration."""
        task_config = TaskConfig(name, input, function, output, **properties)
        cls._python_config.tasks[task_config.name] = task_config
        cls.__compile_configs()
        return cls._applied_config.tasks[task_config.name]

    @classmethod
    def add_default_task(
        cls,
        input: Union[DataNodeConfig, List[DataNodeConfig]],
        function,
        output: Union[DataNodeConfig, List[DataNodeConfig]],
        **properties,
    ):
        """Configures the default task configuration."""
        task_config = TaskConfig(_Config.DEFAULT_KEY, input, function, output, **properties)
        cls._python_config.tasks[task_config.name] = task_config
        cls.__compile_configs()
        return cls._applied_config.tasks[_Config.DEFAULT_KEY]

    @classmethod
    def add_pipeline(cls, name: str, tasks_configs: Union[TaskConfig, List[TaskConfig]], **properties):
        """Adds a new pipeline configuration."""
        pipeline_config = PipelineConfig(name, tasks_configs, **properties)
        cls._python_config.pipelines[pipeline_config.name] = pipeline_config
        cls.__compile_configs()
        return cls._applied_config.pipelines[pipeline_config.name]

    @classmethod
    def add_default_pipeline(cls, tasks_configs: Union[TaskConfig, List[TaskConfig]], **properties):
        """Configures the default pipeline configuration."""
        pipeline_config = PipelineConfig(_Config.DEFAULT_KEY, tasks_configs, **properties)
        cls._python_config.pipelines[_Config.DEFAULT_KEY] = pipeline_config
        cls.__compile_configs()
        return cls._applied_config.pipelines[_Config.DEFAULT_KEY]

    @classmethod
    def add_scenario(
        cls,
        name: str,
        pipelines: List[PipelineConfig],
        frequency: Optional[Frequency] = None,
        comparators: Optional[Dict[str, Union[List[Callable], Callable]]] = None,
        **properties,
    ):
        """Adds a new scenario configuration."""
        scenario_config = ScenarioConfig(name, pipelines, frequency=frequency, comparators=comparators, **properties)
        cls._python_config.scenarios[scenario_config.name] = scenario_config
        cls.__compile_configs()
        return cls._applied_config.scenarios[scenario_config.name]

    @classmethod
    def add_default_scenario(
        cls,
        pipelines: List[PipelineConfig],
        frequency: Optional[Frequency] = None,
        comparators: Optional[Dict[str, Union[List[Callable], Callable]]] = None,
        **properties,
    ):
        """Configures the default scenario configuration."""
        scenario_config = ScenarioConfig(
            _Config.DEFAULT_KEY, pipelines, frequency=frequency, comparators=comparators, **properties
        )
        cls._python_config.scenarios[_Config.DEFAULT_KEY] = scenario_config
        cls.__compile_configs()
        return cls._applied_config.scenarios[_Config.DEFAULT_KEY]

    @classmethod
    def _load_environment_file_config(cls):
        if config_filename := os.environ.get(cls.ENVIRONMENT_VARIABLE_NAME_WITH_CONFIG_PATH):
            logging.info(f"Filename '{config_filename}' provided by environment variable")
            cls._env_file_config = TomlSerializer().read(config_filename)
            logging.info(f"Successful loaded configuration filename '{config_filename}'")

    @classmethod
    def __compile_configs(cls):
        Config._load_environment_file_config()
        cls._applied_config = _Config.default_config()
        if cls._python_config:
            cls._applied_config.update(cls._python_config)
        if cls._file_config:
            cls._applied_config.update(cls._file_config)
        if cls._env_file_config:
            cls._applied_config.update(cls._env_file_config)
        cls.collector = Checker().check(cls._applied_config)
        cls.__log_message(cls)

    @staticmethod
    def __log_message(config):
        for issue in config.collector.warnings:
            logging.warning(str(issue))
        for issue in config.collector.infos:
            logging.info(str(issue))
        for issue in config.collector.errors:
            logging.error(str(issue))
        if len(config.collector.errors) != 0:
            raise ConfigurationIssueError


Config._load_environment_file_config()
