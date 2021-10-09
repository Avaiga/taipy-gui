__all__ = ["TaskScheduler"]

import logging
import uuid
from collections import abc
from concurrent.futures import Future, ProcessPoolExecutor
from functools import partial
from typing import Any, Dict, List, Union

from taipy.task.task import Task

from ...data import DataSource
from .executor import FutureExecutor
from .job import Job, JobId
from taipy.configuration import ConfigurationManager


class TaskScheduler:
    """
    Create and schedule Jobs from Task and keep their states
    """

    def __init__(self):
        self.__jobs: Dict[JobId, Job] = {}
        self.__executor = self.__create_executor()

    def submit(self, task: Task) -> JobId:
        """
        Submit a task that should be executed as a Job and return its JobId

        The result of the Task executed is provided to its output data source
        by mapping each element with each output data source of the Task.
        If the number of output data sources is
        different to the number of Task results, we do nothing

        If an error happens when the result is provided to a data source, we ignore it
        and continue to the next data source
        """
        self.__execute_function_and_write_outputs(task)
        return self.__create_job(task)

    def __create_job(self, task: Task) -> JobId:
        job = Job(id=JobId(f"job_id_{task.id}_{uuid.uuid4()}"), task_id=task.id)
        self.__jobs[job.id] = job
        return job.id

    def __execute_function_and_write_outputs(self, task):
        future = self.__executor.submit(task.function, *[i.get() for i in task.input.values()])
        future.add_done_callback(partial(_WriteResultInDataSource.write, task.output.values()))

    @staticmethod
    def __create_executor():
        if ConfigurationManager.task_scheduler_configuration.parallel_execution:
            return ProcessPoolExecutor(
                ConfigurationManager.task_scheduler_configuration.max_number_of_parallel_execution
            )
        return FutureExecutor()


class _WriteResultInDataSource:
    @classmethod
    def write(cls, outputs: List[DataSource], future: Future):
        results = [future.result()] if len(outputs) == 1 else future.result()
        cls._write(results, outputs)

    @classmethod
    def _write(cls, results, outputs):
        if len(results) == len(outputs):
            for res, output in zip(results, outputs):
                cls._write_result_in_output(res, output)
        else:
            logging.error("Error, wrong number of result or task output")

    @staticmethod
    def _write_result_in_output(result: Any, output: DataSource):
        try:
            output.write(result)
        except Exception as e:
            logging.error(f"Error on writing output {e}")
