import multiprocessing
import uuid
from functools import partial
from time import sleep

from taipy.configuration import ConfigurationManager
from taipy.data import EmbeddedDataSource
from taipy.data.scope import Scope
from taipy.task import Task
from taipy.task.scheduler import TaskScheduler


def multiply(nb1: float, nb2: float):
    return nb1 * nb2


def lock_multiply(lock, nb1: float, nb2: float):
    with lock:
        return multiply(nb1, nb2)


def test_scheduled_task():
    task_scheduler = TaskScheduler()
    task = _create_task_entity(multiply)

    task_scheduler.submit(task)
    assert task.output0.get() == 42


def test_scheduled_task_that_return_multiple_outputs():
    def return_2tuple(nb1, nb2):
        return multiply(nb1, nb2), multiply(nb1, nb2) / 2

    def return_list(nb1, nb2):
        return [multiply(nb1, nb2), multiply(nb1, nb2) / 2]

    task_scheduler = TaskScheduler()

    with_tuple = _create_task_entity(return_2tuple, 2)
    with_list = _create_task_entity(return_list, 2)

    task_scheduler.submit(with_tuple)
    task_scheduler.submit(with_list)

    assert with_tuple.output0.get() == with_list.output0.get() == 42
    assert with_tuple.output1.get() == with_list.output1.get() == 21


def test_scheduled_task_returns_single_iterable_output():
    def return_2tuple(nb1, nb2):
        return multiply(nb1, nb2), multiply(nb1, nb2) / 2

    def return_list(nb1, nb2):
        return [multiply(nb1, nb2), multiply(nb1, nb2) / 2]

    task_scheduler = TaskScheduler()
    task_with_tuple = _create_task_entity(return_2tuple, 1)
    task_with_list = _create_task_entity(return_list, 1)

    task_scheduler.submit(task_with_tuple)
    assert task_with_tuple.output0.get() == (42, 21)
    task_scheduler.submit(task_with_list)
    assert task_with_list.output0.get() == [42, 21]


def test_data_source_not_written_due_to_wrong_result_nb():
    def return_2tuple():
        return lambda nb1, nb2: (multiply(nb1, nb2), multiply(nb1, nb2) / 2)

    task_scheduler = TaskScheduler()
    task = _create_task_entity(return_2tuple(), 3)

    task_scheduler.submit(task)
    assert task.output0.get() == 0


def test_error_during_writing_data_source_don_t_stop_writing_on_other_data_source():
    task_scheduler = TaskScheduler()

    task = _create_task_entity(lambda nb1, nb2: (42, 21), 2)
    task.output0.write = None
    task_scheduler.submit(task)

    assert task.output0.get() == 0
    assert task.output1.get() == 21


def test_scheduled_task_in_parallel():
    ConfigurationManager.task_scheduler_configuration.parallel_execution = True
    m = multiprocessing.Manager()
    lock = m.Lock()

    task_scheduler = TaskScheduler()
    task = _create_task_entity(partial(lock_multiply, lock))

    with lock:
        task_scheduler.submit(task)
        assert task.output0.get() == 0

    sleep(1)
    assert task.output0.get() == 42


def test_scheduled_task_multithreading_multiple_task():
    ConfigurationManager.task_scheduler_configuration.parallel_execution = True

    task_scheduler = TaskScheduler()

    m = multiprocessing.Manager()
    lock_1 = m.Lock()
    lock_2 = m.Lock()

    task_1 = _create_task_entity(partial(lock_multiply, lock_1))
    task_2 = _create_task_entity(partial(lock_multiply, lock_2))

    with lock_1:
        with lock_2:
            task_scheduler.submit(task_1)
            task_scheduler.submit(task_2)

            assert task_1.output0.get() == 0
            assert task_2.output0.get() == 0

        sleep(1)
        assert task_1.output0.get() == 0
        assert task_2.output0.get() == 42

    sleep(1)
    assert task_1.output0.get() == 42
    assert task_2.output0.get() == 42


def _create_task_entity(function, nb_outputs=1):
    task_name = str(uuid.uuid4())
    input_ds = [
        EmbeddedDataSource.create("input1", Scope.PIPELINE, data=21),
        EmbeddedDataSource.create("input2", Scope.PIPELINE, data=2),
    ]
    output_ds = [
        EmbeddedDataSource.create(f"output{i}", Scope.PIPELINE, data=0)
        for i in range(nb_outputs)
    ]
    return Task(
        task_name,
        input=input_ds,
        function=function,
        output=output_ds,
    )
