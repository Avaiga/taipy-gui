__all__ = ['TaskScheduler']

import uuid
import logging

from .executor.executor import Executor
from .job import JobId, Job
from .. import TaskEntity


class TaskScheduler:
    """
    Create and schedule Jobs from Task and keep their states
    """
    def __init__(self):
        self._jobs = set()
        self._executor = Executor()

    def submit(self, task: TaskEntity) -> JobId:
        """
        Submit a task that should be executed as a Job
        """
        self._executor.submit(task)
        return self._create_job(task)

    def _create_job(self, task: TaskEntity) -> JobId:
        job = Job(
            id=JobId(f"job_id_{task.id}_{uuid.uuid4()}"),
            task_id=task.id
        )
        self._jobs.add(job)
        logging.info(f"task {task.id} submitted. Job id : {job.id}")
        return job.id

