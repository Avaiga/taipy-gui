import logging
from typing import Dict

from taipy.data import DataSourceEntity
from taipy.data.data_source import DataSource
from taipy.data.manager import DataManager
from taipy.exceptions import NonExistingTaskEntity
from taipy.exceptions.task import NonExistingTask
from taipy.task.task import Task
from taipy.task.task_entity import TaskEntity, TaskId


class TaskManager:
    # This represents the task database.
    task_entities: Dict[(TaskId, TaskEntity)] = {}
    __TASKS: Dict[(str, Task)] = {}
    data_manager = DataManager()

    def delete_all(self):
        self.task_entities: Dict[(TaskId, TaskEntity)] = {}
        self.__TASKS: Dict[(str, Task)] = {}

    def register_task(self, task: Task):
        [
            self.data_manager.register_data_source(data_source)
            for data_source in task.input
        ]
        [
            self.data_manager.register_data_source(data_source)
            for data_source in task.output
        ]
        self.__TASKS[task.name] = task

    def get_task(self, name: str) -> Task:
        try:
            return self.__TASKS[name]
        except KeyError:
            logging.error(f"Task : {name} does not exist.")
            raise NonExistingTask(name)

    def get_tasks(self):
        return self.__TASKS

    def save_task_entity(self, task: TaskEntity):
        logging.info(f"Task : {task.id} created or updated.")
        self.task_entities[task.id] = task

    def create_task_entity(
        self, task: Task, data_source_entities: Dict[DataSource, DataSourceEntity]
    ) -> TaskEntity:
        if data_source_entities is None:
            all_ds: set[DataSource] = set()
            for ds in task.input:
                all_ds.add(ds)
            for ds in task.output:
                all_ds.add(ds)
            data_source_entities = {
                ds: self.data_manager.create_data_source_entity(ds) for ds in all_ds
            }
        input_entities = [data_source_entities[input] for input in task.input]
        output_entities = [data_source_entities[output] for output in task.output]
        task_entity = TaskEntity(
            task.name, input_entities, task.function, output_entities
        )
        self.save_task_entity(task_entity)
        return task_entity

    def get_task_entity(self, task_id: TaskId) -> TaskEntity:
        try:
            return self.task_entities[task_id]
        except KeyError:
            logging.error(f"Task entity : {task_id} does not exist.")
            raise NonExistingTaskEntity(task_id)
