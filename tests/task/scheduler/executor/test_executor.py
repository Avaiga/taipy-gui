import glob
import multiprocessing
import os
from functools import partial
from time import sleep

import pytest

from taipy.common.alias import TaskId
from taipy.config import Config
from taipy.data import Scope
from taipy.data.manager import DataManager
from taipy.task import Job, JobId, Task
from taipy.task.scheduler.executor.executor import Executor


@pytest.fixture(scope="function", autouse=True)
def reset_configuration_singleton():
    yield

    for f in glob.glob("*.p"):
        print(f"deleting file {f}")
        os.remove(f)


def execute(lock):
    with lock:
        ...
    return None


def test_can_execute_parallel():
    m = multiprocessing.Manager()
    lock = m.Lock()

    task_id = TaskId("task_id1")
    task = Task(
        config_name="name",
        input=[],
        function=partial(execute, lock),
        output=[
            DataManager().get_or_create(Config.data_source_configs.create("input1", "pickle", Scope.PIPELINE, data=21))
        ],
        id=task_id,
    )
    job_id = JobId("id1")
    job = Job(job_id, task)

    executor = Executor(True, 1)

    with lock:
        assert executor.can_execute()
        executor.execute(job)
        assert not executor.can_execute()

    sleep(1)
    executor.can_execute()


def test_can_execute_parallel_multiple_submit():
    m = multiprocessing.Manager()
    lock = m.Lock()

    task_id = TaskId("task_id1")
    task = Task(config_name="name", input=[], function=partial(execute, lock), output=[], id=task_id)
    job_id = JobId("id1")
    job = Job(job_id, task)

    executor = Executor(True, 2)

    with lock:
        assert executor.can_execute()
        executor.execute(job)
        assert executor.can_execute()


def test_can_execute_synchronous():
    task_id = TaskId("task_id1")
    task = Task(config_name="name", input=[], function=print, output=[], id=task_id)
    job_id = JobId("id1")
    job = Job(job_id, task)

    executor = Executor(False, None)

    assert executor.can_execute()
    executor.execute(job)
    assert executor.can_execute()
