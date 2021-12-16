import itertools
import logging
from typing import Dict, List, Optional

from taipy.common.alias import PipelineId, ScenarioId, TaskId
from taipy.config import TaskConfig
from taipy.data import Scope
from taipy.data.manager import DataManager
from taipy.exceptions import ModelNotFound, NonExistingTask
from taipy.exceptions.task import MultipleTaskFromSameConfigWithSameParent
from taipy.task import TaskScheduler
from taipy.task.repository import TaskRepository
from taipy.task.task import Task


class TaskManager:
    """
    The Task Manager saves and retrieves Tasks.

    Attributes:
        tasks (Dict[(TaskId, Task)]): A dictionary that associates every task with its identifier.
        task_scheduler (TaskScheduler): The task scheduler that can run tasks.
        data_manager (DataManager): The Data Manager that interacts with data sources.
        repository (TaskRepository): The repository where tasks are saved.
    """

    tasks: Dict[(TaskId, Task)] = {}
    task_scheduler = TaskScheduler()
    data_manager = task_scheduler.data_manager
    repository = TaskRepository()

    def delete_all(self):
        """
        Deletes all the persisted tasks.
        """
        self.repository.delete_all()

    def delete(self, task_id: TaskId):
        """Deletes the cycle provided as parameter.

        Parameters:
            task_id (str): identifier of the task to delete.
        Raises:
            ModelNotFound error if no task corresponds to task_id.
        """
        self.repository.delete(task_id)

    def get_all(self):
        """
        Returns the list of all existing tasks.

        Returns:
            List: The list of tasks handled by this Task Manager.
        """
        return self.repository.load_all()

    def set(self, task: Task):
        """
        Saves or updates a task.

        Args:
            task (Task): The task to save.
        """
        logging.info(f"Task: {task.id} created or updated.")
        self.__save_data_sources(task.input.values())
        self.__save_data_sources(task.output.values())
        self.repository.save(task)

    def get_or_create(
        self,
        task_config: TaskConfig,
        scenario_id: Optional[ScenarioId] = None,
        pipeline_id: Optional[PipelineId] = None,
    ) -> Task:
        """Returns a task created from the provided task configuration.

        If no task exists for that task configuration, in the provided `scenario_id` and `pipeline_id`, then
        a new task is created and returned.

        Args:
            task_config (TaskConfig): The task configuration object.
            scenario_id (ScenarioId): The identifier of the scenario creating the task.
            pipeline_id (PipelineId): The identifier of the pipeline creating the task.

        Returns:
            A task, potentially new, that is created for that task configuration.

        Raises:
            MultipleTaskFromSameConfigWithSameParent: if more than one task already exists with the same
                configuration, and the same parent id (scenario or pipeline identifier, depending on the
                scope of the data source). TODO: This comment makes no sense - Data Source scope
        """
        data_sources = {
            ds_config: self.data_manager.get_or_create(ds_config, scenario_id, pipeline_id)
            for ds_config in set(itertools.chain(task_config.input, task_config.output))
        }
        scope = min(ds.scope for ds in data_sources.values()) if len(data_sources) != 0 else Scope.GLOBAL
        parent_id = pipeline_id if scope == Scope.PIPELINE else scenario_id if scope == Scope.SCENARIO else None
        tasks_from_config_name = self._get_all_by_config_name(task_config.name)
        tasks_from_parent = [task for task in tasks_from_config_name if task.parent_id == parent_id]
        if len(tasks_from_parent) == 1:
            return tasks_from_parent[0]
        elif len(tasks_from_parent) > 1:
            logging.error("Multiple tasks from same config exist with the same parent_id.")
            raise MultipleTaskFromSameConfigWithSameParent
        else:
            inputs = [data_sources[input_config] for input_config in task_config.input]
            outputs = [data_sources[output_config] for output_config in task_config.output]
            task = Task(task_config.name, inputs, task_config.function, outputs, parent_id=parent_id)
            self.set(task)
            return task

    def get(self, task_id: TaskId) -> Task:
        """
        Gets a task given its identifier.

        Args:
            task_id (TaskId): The task identifier.

        Returns:
            The task with the provided identifier.

        Raises:
            ModelNotFound: if no task corresponds to `task_id`.
        """
        try:
            if opt_task := self.repository.load(task_id):
                return opt_task
            else:
                logging.error(f"Task: {task_id} does not exist.")
                raise NonExistingTask(task_id)
        except ModelNotFound:
            logging.error(f"Task: {task_id} does not exist.")
            raise NonExistingTask(task_id)

    def __save_data_sources(self, data_sources):
        for i in data_sources:
            self.data_manager.set(i)

    def _get_all_by_config_name(self, config_name: str) -> List[Task]:
        """
        Returns the list of all existing tasks with the corresponding config name.

        Args:
             config_name (str) : task config's name.

        Returns:
            List of tasks of this config name
        """
        return self.repository.search_all("config_name", config_name)

    def hard_delete(
        self, task_id: TaskId, scenario_id: Optional[ScenarioId] = None, pipeline_id: Optional[PipelineId] = None
    ):
        """
        Deletes the task given as parameter and the nested data sources, and jobs.

        Deletes the task given as parameter and propagate the hard deletion. The hard delete is propagated to a
        nested data sources if the data sources is not shared by another pipeline or if a scenario id is given as
        parameter, by another scenario.

        Parameters:
        task_id (TaskId): identifier of the task to hard delete.
        pipeline_id (PipelineId) : identifier of the optional parent pipeline.
        scenario_id (ScenarioId) : identifier of the optional parent scenario.

        Raises:
        ModelNotFound error if no pipeline corresponds to pipeline_id.
        """
        task = self.get(task_id)
        jobs = self.task_scheduler.get_jobs()

        if scenario_id:
            self.remove_if_parent_id_eq(task.input.values(), scenario_id)
            self.remove_if_parent_id_eq(task.output.values(), scenario_id)
        if pipeline_id:
            self.remove_if_parent_id_eq(task.input.values(), pipeline_id)
            self.remove_if_parent_id_eq(task.output.values(), pipeline_id)

        for job in jobs:
            if job.task.id == task.id:
                self.task_scheduler.delete(job)
        self.delete(task_id)

    def remove_if_parent_id_eq(self, data_sources, id_):
        for data_source in data_sources:
            if data_source.parent_id == id_:
                self.data_manager.delete(data_source.id)
