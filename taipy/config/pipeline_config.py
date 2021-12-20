from copy import copy
from typing import Any, Dict, List, Optional, Union

from taipy.common import protect_name
from taipy.config.task_config import TaskConfig


class PipelineConfig:
    """
    Holds all the configuration fields needed to create actual pipelines from the PipelineConfig.

    Attributes:
        name (str):  Unique name as an identifier of the pipeline config.
            We strongly recommend to use lowercase alphanumeric characters, dash character '-', or underscore character
            '_'. Note that other characters are replaced according the following rules :
            - Space characters are replaced by underscore characters ('_').
            - Unicode characters are replaced by a corresponding alphanumeric character using the Unicode library.
            - Other characters are replaced by dash characters ('-').
        tasks (list): List of task configs. Default value: [].
        properties (dict): Dictionary of additional properties.
    """

    TASK_KEY = "tasks"

    def __init__(self, name: str, tasks: Union[TaskConfig, List[TaskConfig]] = None, **properties):
        self.name = protect_name(name)
        self.properties = properties
        if tasks:
            self.tasks = [tasks] if isinstance(tasks, TaskConfig) else copy(tasks)
        else:
            self.tasks = []

    def __getattr__(self, item: str) -> Optional[Any]:
        return self.properties.get(item)

    def __copy__(self):
        return PipelineConfig(self.name, copy(self.tasks), **copy(self.properties))

    @classmethod
    def default_config(cls, name):
        return PipelineConfig(name, [])

    @property
    def tasks_configs(self) -> List[TaskConfig]:
        return self.tasks

    def to_dict(self):
        return {self.TASK_KEY: self.tasks, **self.properties}

    @classmethod
    def from_dict(cls, name: str, config_as_dict: Dict[str, Any], task_configs: Dict[str, TaskConfig]):
        config = PipelineConfig(name)
        config.name = protect_name(name)
        if tasks := config_as_dict.pop(cls.TASK_KEY, None):
            config.tasks = [task_configs[task_id] for task_id in tasks if task_id in task_configs]
        config.properties = config_as_dict
        return config

    def update(self, config_as_dict, default_pipeline_cfg=None):
        self.tasks = config_as_dict.pop(self.TASK_KEY, self.tasks) or default_pipeline_cfg.tasks
        if self.tasks is None and default_pipeline_cfg:
            self.tasks = default_pipeline_cfg.tasks
        self.properties.update(config_as_dict)
