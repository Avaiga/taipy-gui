from datetime import datetime, timedelta

import pytest

from taipy.common import utils
from taipy.common.alias import PipelineId, ScenarioId, TaskId
from taipy.common.frequency import Frequency
from taipy.config.config import Config
from taipy.data import InMemoryDataSource, Scope
from taipy.exceptions import NonExistingTask
from taipy.exceptions.pipeline import NonExistingPipeline
from taipy.exceptions.scenario import (
    DeletingMasterScenario,
    DifferentScenarioConfigs,
    InsufficientScenarioToCompare,
    NonExistingComparator,
    NonExistingScenario,
    NonExistingScenarioConfig,
)
from taipy.pipeline import Pipeline
from taipy.scenario.manager import ScenarioManager
from taipy.scenario.scenario import Scenario
from taipy.task import Task, TaskScheduler
from tests.taipy.utils.NotifyMock import NotifyMock


def test_set_and_get_scenario(cycle):
    scenario_id_1 = ScenarioId("scenario_id_1")
    scenario_1 = Scenario("scenario_name_1", [], {}, scenario_id_1)

    input_2 = InMemoryDataSource("foo", Scope.PIPELINE)
    output_2 = InMemoryDataSource("foo", Scope.PIPELINE)
    task_name = "task"
    task_2 = Task(task_name, [input_2], print, [output_2], TaskId("task_id_2"))
    pipeline_name_2 = "pipeline_name_2"
    pipeline_2 = Pipeline(pipeline_name_2, {}, [task_2], PipelineId("pipeline_id_2"))
    scenario_id_2 = ScenarioId("scenario_id_2")
    scenario_2 = Scenario("scenario_name_2", [pipeline_2], {}, scenario_id_2, True, cycle)

    pipeline_3 = Pipeline("pipeline_name_3", {}, [], PipelineId("pipeline_id_3"))
    scenario_3_with_same_id = Scenario("scenario_name_3", [pipeline_3], {}, scenario_id_1, False, cycle)

    # No existing scenario
    scenario_manager = ScenarioManager()
    assert len(scenario_manager.get_all()) == 0
    with pytest.raises(NonExistingScenario):
        scenario_manager.get(scenario_id_1)
    with pytest.raises(NonExistingScenario):
        scenario_manager.get(scenario_id_2)

    # Save one scenario. We expect to have only one scenario stored
    scenario_manager.set(scenario_1)
    assert len(scenario_manager.get_all()) == 1
    assert scenario_manager.get(scenario_id_1).id == scenario_1.id
    assert scenario_manager.get(scenario_id_1).config_name == scenario_1.config_name
    assert len(scenario_manager.get(scenario_id_1).pipelines) == 0
    with pytest.raises(NonExistingScenario):
        scenario_manager.get(scenario_id_2)

    # Save a second scenario. Now, we expect to have a total of two scenarios stored
    scenario_manager.pipeline_manager.task_manager.set(task_2)
    scenario_manager.pipeline_manager.set(pipeline_2)
    scenario_manager.cycle_manager.set(cycle)
    scenario_manager.set(scenario_2)
    assert len(scenario_manager.get_all()) == 2
    assert scenario_manager.get(scenario_id_1).id == scenario_1.id
    assert scenario_manager.get(scenario_id_1).config_name == scenario_1.config_name
    assert len(scenario_manager.get(scenario_id_1).pipelines) == 0
    assert scenario_manager.get(scenario_id_2).id == scenario_2.id
    assert scenario_manager.get(scenario_id_2).config_name == scenario_2.config_name
    assert len(scenario_manager.get(scenario_id_2).pipelines) == 1
    assert scenario_manager.task_manager.get(task_2.id).id == task_2.id
    assert scenario_manager.get(scenario_id_2).cycle == cycle
    assert scenario_manager.cycle_manager.get(cycle.id).id == cycle.id

    # We save the first scenario again. We expect nothing to change
    scenario_manager.set(scenario_1)
    assert len(scenario_manager.get_all()) == 2
    assert scenario_manager.get(scenario_id_1).id == scenario_1.id
    assert scenario_manager.get(scenario_id_1).config_name == scenario_1.config_name
    assert len(scenario_manager.get(scenario_id_1).pipelines) == 0
    assert scenario_manager.get(scenario_id_2).id == scenario_2.id
    assert scenario_manager.get(scenario_id_2).config_name == scenario_2.config_name
    assert len(scenario_manager.get(scenario_id_2).pipelines) == 1
    assert scenario_manager.task_manager.get(task_2.id).id == task_2.id
    assert scenario_manager.cycle_manager.get(cycle.id).id == cycle.id

    # We save a third scenario with same id as the first one.
    # We expect the first scenario to be updated
    scenario_manager.pipeline_manager.task_manager.set(scenario_2.pipelines[pipeline_name_2].tasks[task_name])
    scenario_manager.pipeline_manager.set(pipeline_3)
    scenario_manager.set(scenario_3_with_same_id)
    assert len(scenario_manager.get_all()) == 2
    assert scenario_manager.get(scenario_id_1).id == scenario_1.id
    assert scenario_manager.get(scenario_id_1).config_name == scenario_3_with_same_id.config_name
    assert len(scenario_manager.get(scenario_id_1).pipelines) == 1
    assert scenario_manager.get(scenario_id_1).cycle == cycle
    assert scenario_manager.get(scenario_id_2).id == scenario_2.id
    assert scenario_manager.get(scenario_id_2).config_name == scenario_2.config_name
    assert len(scenario_manager.get(scenario_id_2).pipelines) == 1
    assert scenario_manager.task_manager.get(task_2.id).id == task_2.id


def test_create_and_delete_scenario():
    creation_date_1 = datetime.now()
    creation_date_2 = creation_date_1 + timedelta(minutes=10)

    scenario_manager = ScenarioManager()

    scenario_manager.delete_all()
    assert len(scenario_manager.get_all()) == 0

    scenario_config = Config.add_scenario("sc", [], Frequency.DAILY)

    scenario_1 = scenario_manager.create(scenario_config, creation_date=creation_date_1)
    assert scenario_1.config_name == "sc"
    assert scenario_1.pipelines == {}
    assert scenario_1.cycle.frequency == Frequency.DAILY
    assert scenario_1.master_scenario
    assert scenario_1.cycle.creation_date == creation_date_1
    assert scenario_1.cycle.start_date.date() == creation_date_1.date()
    assert scenario_1.cycle.end_date.date() == creation_date_1.date()

    with pytest.raises(DeletingMasterScenario):
        scenario_manager.delete(scenario_1.id)

    scenario_2 = scenario_manager.create(scenario_config, creation_date=creation_date_2)
    assert scenario_2.config_name == "sc"
    assert scenario_2.pipelines == {}
    assert scenario_2.cycle.frequency == Frequency.DAILY
    assert not scenario_2.master_scenario
    assert scenario_2.cycle.creation_date == creation_date_1
    assert scenario_2.cycle.start_date.date() == creation_date_2.date()
    assert scenario_2.cycle.end_date.date() == creation_date_2.date()

    assert scenario_1 != scenario_2
    assert scenario_1.cycle == scenario_2.cycle

    assert len(scenario_manager.get_all()) == 2
    scenario_manager.delete(scenario_2.id)
    assert len(scenario_manager.get_all()) == 1
    with pytest.raises(DeletingMasterScenario):
        scenario_manager.delete(scenario_1.id)
    with pytest.raises(NonExistingScenario):
        scenario_manager.get(scenario_2.id)


def mult_by_2(nb: int):
    return nb * 2


def mult_by_3(nb: int):
    return nb * 3


def mult_by_4(nb: int):
    return nb * 4


def test_scenario_manager_only_creates_data_source_once():
    scenario_manager = ScenarioManager()
    pipeline_manager = scenario_manager.pipeline_manager
    task_manager = scenario_manager.task_manager
    data_manager = scenario_manager.data_manager
    cycle_manager = scenario_manager.cycle_manager

    ds_config_1 = Config.add_data_source("foo", "in_memory", Scope.PIPELINE, default_data=1)
    ds_config_2 = Config.add_data_source("bar", "in_memory", Scope.SCENARIO, default_data=0)
    ds_config_6 = Config.add_data_source("baz", "in_memory", Scope.PIPELINE, default_data=0)
    ds_config_4 = Config.add_data_source("qux", "in_memory", Scope.PIPELINE, default_data=0)

    task_mult_by_2_config = Config.add_task("mult by 2", [ds_config_1], mult_by_2, ds_config_2)
    task_mult_by_3_config = Config.add_task("mult by 3", [ds_config_2], mult_by_3, ds_config_6)
    task_mult_by_4_config = Config.add_task("mult by 4", [ds_config_1], mult_by_4, ds_config_4)
    pipeline_config_1 = Config.add_pipeline("by 6", [task_mult_by_2_config, task_mult_by_3_config])
    # ds_1 ---> mult by 2 ---> ds_2 ---> mult by 3 ---> ds_6
    pipeline_config_2 = Config.add_pipeline("by 4", [task_mult_by_4_config])
    # ds_1 ---> mult by 4 ---> ds_4
    scenario_config = Config.add_scenario("Awesome scenario", [pipeline_config_1, pipeline_config_2], Frequency.DAILY)

    assert len(data_manager.get_all()) == 0
    assert len(task_manager.get_all()) == 0
    assert len(pipeline_manager.get_all()) == 0
    assert len(scenario_manager.get_all()) == 0
    assert len(cycle_manager.get_all()) == 0

    scenario = scenario_manager.create(scenario_config)

    assert len(data_manager.get_all()) == 5
    assert len(task_manager.get_all()) == 3
    assert len(pipeline_manager.get_all()) == 2
    assert len(scenario_manager.get_all()) == 1
    assert scenario.foo.read() == 1
    assert scenario.bar.read() == 0
    assert scenario.baz.read() == 0
    assert scenario.qux.read() == 0
    assert scenario.by_6.get_sorted_tasks()[0][0].config_name == task_mult_by_2_config.name
    assert scenario.by_6.get_sorted_tasks()[1][0].config_name == task_mult_by_3_config.name
    assert scenario.by_4.get_sorted_tasks()[0][0].config_name == task_mult_by_4_config.name
    assert scenario.cycle.frequency == Frequency.DAILY


def test_notification_subscribe_unsubscribe(mocker):
    scenario_manager = ScenarioManager()

    scenario_config = Config.add_scenario(
        "Awesome scenario",
        [
            Config.add_pipeline(
                "by 6",
                [
                    Config.add_task(
                        "mult by 2",
                        [Config.add_data_source("foo", "in_memory", Scope.PIPELINE, default_data=1)],
                        mult_by_2,
                        Config.add_data_source("bar", "in_memory", Scope.SCENARIO, default_data=0),
                    )
                ],
            )
        ],
    )

    scenario = scenario_manager.create(scenario_config)

    notify_1 = NotifyMock(scenario)
    notify_2 = NotifyMock(scenario)
    mocker.patch.object(utils, "load_fct", side_effect=[notify_1, notify_2])

    # test subscribing notification
    scenario_manager.subscribe(notify_1, scenario)
    scenario_manager.submit(scenario.id)
    notify_1.assert_called_3_times()

    notify_1.reset()

    # test unsubscribing notification
    # test notis subscribe only on new jobs
    scenario_manager.unsubscribe(notify_1, scenario)
    scenario_manager.subscribe(notify_2, scenario)
    scenario_manager.submit(scenario.id)

    notify_1.assert_not_called()
    notify_2.assert_called_3_times()

    with pytest.raises(KeyError):
        scenario_manager.unsubscribe(notify_1, scenario)
    scenario_manager.unsubscribe(notify_2, scenario)


def test_scenario_notification_subscribe_all():
    scenario_manager = ScenarioManager()
    scenario_config = Config.add_scenario(
        "Awesome scenario",
        [
            Config.add_pipeline(
                "by 6",
                [
                    Config.add_task(
                        "mult by 2",
                        [Config.add_data_source("foo", "in_memory", Scope.PIPELINE, default_data=1)],
                        mult_by_2,
                        Config.add_data_source("bar", "in_memory", Scope.SCENARIO, default_data=0),
                    )
                ],
            )
        ],
    )

    scenario = ScenarioManager().create(scenario_config)
    scenario_config.name = "other scenario"

    other_scenario = ScenarioManager().create(scenario_config)

    notify_1 = NotifyMock(scenario)

    scenario_manager.subscribe(notify_1)

    assert len(scenario_manager.get(scenario.id).subscribers) == 1
    assert len(scenario_manager.get(other_scenario.id).subscribers) == 1


def test_get_set_master_scenario():
    scenario_manager = ScenarioManager()
    cycle_manager = scenario_manager.cycle_manager

    cycle_1 = cycle_manager.create(Frequency.DAILY)

    scenario_1 = Scenario("sc_1", [], {}, ScenarioId("sc_1"), is_master=False, cycle=cycle_1)
    scenario_2 = Scenario("sc_2", [], {}, ScenarioId("sc_2"), is_master=False, cycle=cycle_1)

    scenario_manager.delete_all()
    cycle_manager.delete_all()

    assert len(scenario_manager.get_all()) == 0
    assert len(cycle_manager.get_all()) == 0

    cycle_manager.set(cycle_1)

    scenario_manager.set(scenario_1)
    scenario_manager.set(scenario_2)

    assert len(scenario_manager.get_all_masters()) == 0
    assert len(scenario_manager.get_all_by_cycle(cycle_1)) == 2

    scenario_manager.set_master(scenario_1)

    assert len(scenario_manager.get_all_masters()) == 1
    assert len(scenario_manager.get_all_by_cycle(cycle_1)) == 2
    assert scenario_manager.get_master(cycle_1) == scenario_1

    scenario_manager.set_master(scenario_2)

    assert len(scenario_manager.get_all_masters()) == 1
    assert len(scenario_manager.get_all_by_cycle(cycle_1)) == 2
    assert scenario_manager.get_master(cycle_1) == scenario_2


def test_hard_delete():
    scenario_manager = ScenarioManager()
    pipeline_manager = scenario_manager.pipeline_manager
    task_manager = scenario_manager.task_manager
    task_scheduler = task_manager.task_scheduler
    data_manager = scenario_manager.data_manager

    ds_input_config = Config.add_data_source("my_input", "in_memory", scope=Scope.SCENARIO, default_data="testing")
    ds_output_config = Config.add_data_source("my_output", "in_memory", scope=Scope.SCENARIO)
    task_config = Config.add_task("task_config", ds_input_config, print, ds_output_config)
    pipeline_config = Config.add_pipeline("pipeline_config", [task_config])
    scenario_config = Config.add_scenario("scenario_config", [pipeline_config])
    scenario = scenario_manager.create(scenario_config)
    scenario_manager.submit(scenario.id)

    # test delete relevant entities with scenario scope
    assert len(task_manager.get_all()) == 1
    assert len(pipeline_manager.get_all()) == 1
    assert len(scenario_manager.get_all()) == 1
    assert len(data_manager.get_all()) == 2
    assert len(task_scheduler.get_jobs()) == 1
    scenario_manager.hard_delete(scenario.id)
    assert len(scenario_manager.get_all()) == 0
    assert len(pipeline_manager.get_all()) == 0
    assert len(task_manager.get_all()) == 0
    assert len(data_manager.get_all()) == 0
    assert len(task_scheduler.get_jobs()) == 0

    scenario_manager.delete_all()
    pipeline_manager.delete_all()
    data_manager.delete_all()
    task_manager.delete_all()
    task_scheduler.delete_all()

    ds_input_config_1 = Config.add_data_source("my_input_1", "in_memory", scope=Scope.PIPELINE, default_data="testing")
    ds_output_config_1 = Config.add_data_source("my_output_1", "in_memory")
    task_config_1 = Config.add_task("task_config_1", ds_input_config_1, print, ds_output_config_1)
    pipeline_config_1 = Config.add_pipeline("pipeline_config_2", [task_config_1])
    scenario_config_1 = Config.add_scenario("scenario_config_2", [pipeline_config_1])
    scenario_1 = scenario_manager.create(scenario_config_1)
    scenario_manager.submit(scenario_1.id)

    # test delete relevant entities with pipeline scope
    assert len(task_manager.get_all()) == 1
    assert len(pipeline_manager.get_all()) == 1
    assert len(scenario_manager.get_all()) == 1
    assert len(data_manager.get_all()) == 2
    assert len(task_scheduler.get_jobs()) == 1
    scenario_manager.hard_delete(scenario_1.id)
    assert len(scenario_manager.get_all()) == 0
    assert len(pipeline_manager.get_all()) == 0
    assert len(task_manager.get_all()) == 0
    assert len(data_manager.get_all()) == 0
    assert len(task_scheduler.get_jobs()) == 0

    ds_input_config_2 = Config.add_data_source("my_input_2", "in_memory", scope=Scope.PIPELINE, default_data="testing")
    ds_output_config_2 = Config.add_data_source("my_output_2", "in_memory", scope=Scope.SCENARIO)
    task_config_2 = Config.add_task("task_config_2", ds_input_config_2, print, ds_output_config_2)
    pipeline_config_2 = Config.add_pipeline("pipeline_config_2", [task_config_2])
    scenario_config_2 = Config.add_scenario("scenario_config_2", [pipeline_config_2])
    scenario_2 = scenario_manager.create(scenario_config_2)
    scenario_manager.submit(scenario_2.id)

    # test delete relevant entities with pipeline scope
    assert len(task_manager.get_all()) == 1
    assert len(pipeline_manager.get_all()) == 1
    assert len(scenario_manager.get_all()) == 1
    assert len(data_manager.get_all()) == 2
    assert len(task_scheduler.get_jobs()) == 1
    scenario_manager.hard_delete(scenario_2.id)  # Do not delete because of pipeline scope
    assert len(scenario_manager.get_all()) == 0
    assert len(pipeline_manager.get_all()) == 0
    assert len(task_manager.get_all()) == 0
    assert len(data_manager.get_all()) == 1
    assert len(task_scheduler.get_jobs()) == 0

    scenario_manager.delete_all()
    pipeline_manager.delete_all()
    data_manager.delete_all()
    task_manager.delete_all()
    task_scheduler.delete_all()

    ds_input_config_3 = Config.add_data_source(
        "my_input_3", "in_memory", scope=Scope.BUSINESS_CYCLE, default_data="testing"
    )
    ds_output_config_3 = Config.add_data_source("my_output_3", "in_memory", scope=Scope.BUSINESS_CYCLE)
    task_config_3 = Config.add_task("task_config", ds_input_config_3, print, ds_output_config_3)
    pipeline_config_3 = Config.add_pipeline("pipeline_config", [task_config_3])
    scenario_config_3 = Config.add_scenario("scenario_config_3", [pipeline_config_3])
    scenario_3 = scenario_manager.create(scenario_config_3)
    scenario_4 = scenario_manager.create(scenario_config_3)
    scenario_manager.submit(scenario_3.id)
    scenario_manager.submit(scenario_4.id)

    # test delete relevant entities with cycle scope
    assert len(scenario_manager.get_all()) == 2
    assert len(pipeline_manager.get_all()) == 1
    assert len(task_manager.get_all()) == 1
    assert len(data_manager.get_all()) == 2
    assert len(task_scheduler.get_jobs()) == 2
    scenario_manager.hard_delete(scenario_3.id)  # Only delete scenario 3
    assert len(scenario_manager.get_all()) == 1
    assert len(pipeline_manager.get_all()) == 1
    assert len(task_manager.get_all()) == 1
    assert len(data_manager.get_all()) == 2
    assert len(task_scheduler.get_jobs()) == 2
    assert scenario_manager.get(scenario_4.id) is not None

    scenario_manager.delete_all()
    pipeline_manager.delete_all()
    data_manager.delete_all()
    task_manager.delete_all()
    task_scheduler.delete_all()

    ds_input_config_4 = Config.add_data_source("my_input_4", "in_memory", scope=Scope.GLOBAL, default_data="testing")
    ds_output_config_4 = Config.add_data_source("my_output_4", "in_memory", scope=Scope.GLOBAL)
    task_config_4 = Config.add_task("task_config_4", ds_input_config_4, print, ds_output_config_4)
    pipeline_config_4 = Config.add_pipeline("pipeline_config", [task_config_4])
    scenario_config_4 = Config.add_scenario("scenario_config_4", [pipeline_config_4])
    scenario_5 = scenario_manager.create(scenario_config_4)
    scenario_6 = scenario_manager.create(scenario_config_4)
    scenario_manager.submit(scenario_5.id)
    scenario_manager.submit(scenario_6.id)

    # test delete relevant entities with global scope
    assert len(scenario_manager.get_all()) == 2
    assert len(pipeline_manager.get_all()) == 1
    assert len(task_manager.get_all()) == 1
    assert len(data_manager.get_all()) == 2
    assert len(task_scheduler.get_jobs()) == 2
    scenario_manager.hard_delete(scenario_5.id)  # Only delete scenario 5
    assert len(scenario_manager.get_all()) == 1
    assert len(pipeline_manager.get_all()) == 1
    assert len(task_manager.get_all()) == 1
    assert len(data_manager.get_all()) == 2
    assert len(task_scheduler.get_jobs()) == 2
    assert scenario_manager.get(scenario_6.id) is not None


def test_submit():
    data_source_1 = InMemoryDataSource("foo", Scope.PIPELINE, "s1")
    data_source_2 = InMemoryDataSource("bar", Scope.PIPELINE, "s2")
    data_source_3 = InMemoryDataSource("baz", Scope.PIPELINE, "s3")
    data_source_4 = InMemoryDataSource("qux", Scope.PIPELINE, "s4")
    data_source_5 = InMemoryDataSource("quux", Scope.PIPELINE, "s5")
    data_source_6 = InMemoryDataSource("quuz", Scope.PIPELINE, "s6")
    data_source_7 = InMemoryDataSource("corge", Scope.PIPELINE, "s7")
    data_source_8 = InMemoryDataSource("fum", Scope.PIPELINE, "s8")
    task_1 = Task(
        "grault",
        [data_source_1, data_source_2],
        print,
        [data_source_3, data_source_4],
        TaskId("t1"),
    )
    task_2 = Task("garply", [data_source_3], print, [data_source_5], TaskId("t2"))
    task_3 = Task("waldo", [data_source_5, data_source_4], print, [data_source_6], TaskId("t3"))
    task_4 = Task("fred", [data_source_4], print, [data_source_7], TaskId("t4"))
    task_5 = Task("thud", [data_source_6], print, [data_source_8], TaskId("t5"))
    pipeline_1 = Pipeline("plugh", {}, [task_4, task_2, task_1, task_3], PipelineId("p1"))
    pipeline_2 = Pipeline("xyzzy", {}, [task_5], PipelineId("p2"))

    scenario = Scenario(
        "scenario_name",
        [pipeline_2, pipeline_1],
        {},
        ScenarioId("sce_id"),
    )

    scenario_manager = ScenarioManager()
    pipeline_manager = scenario_manager.pipeline_manager
    task_manager = scenario_manager.task_manager

    class MockTaskScheduler(TaskScheduler):
        submit_calls = []

        def submit(self, task: Task, callbacks=None):
            self.submit_calls.append(task.id)
            return super().submit(task, callbacks)

    pipeline_manager.task_scheduler = MockTaskScheduler()

    # scenario does not exists. We expect an exception to be raised
    with pytest.raises(NonExistingScenario):
        scenario_manager.submit(scenario.id)

    # scenario does exist, but pipeline does not exist.
    # We expect an exception to be raised
    scenario_manager.set(scenario)
    with pytest.raises(NonExistingPipeline):
        scenario_manager.submit(scenario.id)

    # scenario and pipeline do exist, but tasks does not exist.
    # We expect an exception to be raised
    pipeline_manager.set(pipeline_1)
    pipeline_manager.set(pipeline_2)
    with pytest.raises(NonExistingTask):
        scenario_manager.submit(scenario.id)

    # scenario, pipeline, and tasks do exist.
    # We expect all the tasks to be submitted once,
    # and respecting specific constraints on the order
    task_manager.set(task_1)
    task_manager.set(task_2)
    task_manager.set(task_3)
    task_manager.set(task_4)
    task_manager.set(task_5)
    scenario_manager.submit(scenario.id)
    submit_calls = pipeline_manager.task_scheduler.submit_calls
    assert len(submit_calls) == 5
    assert set(submit_calls) == {task_1.id, task_2.id, task_4.id, task_3.id, task_5.id}
    assert submit_calls.index(task_2.id) < submit_calls.index(task_3.id)
    assert submit_calls.index(task_1.id) < submit_calls.index(task_3.id)
    assert submit_calls.index(task_1.id) < submit_calls.index(task_2.id)
    assert submit_calls.index(task_1.id) < submit_calls.index(task_4.id)


def test_scenarios_comparison():
    def subtraction(inp, out):
        return inp - out

    def addition(inp, out):
        return inp + out

    scenario_manager = ScenarioManager()
    pipeline_manager = scenario_manager.pipeline_manager
    task_manager = scenario_manager.task_manager
    data_manager = scenario_manager.data_manager

    scenario_manager.delete_all()
    pipeline_manager.delete_all()
    data_manager.delete_all()
    task_manager.delete_all()

    scenario_config = Config.add_scenario(
        "Awesome scenario",
        [
            Config.add_pipeline(
                "by 6",
                [
                    Config.add_task(
                        "mult by 2",
                        [Config.add_data_source("foo", "in_memory", Scope.PIPELINE, default_data=1)],
                        mult_by_2,
                        Config.add_data_source("bar", "in_memory", Scope.SCENARIO, default_data=0),
                    )
                ],
            )
        ],
        comparators={"bar": [subtraction], "foo": [subtraction, addition]},
    )

    assert scenario_config.comparators is not None

    scenario_1 = scenario_manager.create(scenario_config)
    scenario_2 = scenario_manager.create(scenario_config)

    with pytest.raises(InsufficientScenarioToCompare):
        scenario_manager.compare(scenario_1, ds_config_name="bar")

    scenario_3 = Scenario("awesome_scenario_config", [], {})
    with pytest.raises(DifferentScenarioConfigs):
        scenario_manager.compare(scenario_1, scenario_3, ds_config_name="bar")

    scenario_manager.submit(scenario_1.id)
    scenario_manager.submit(scenario_2.id)

    bar_comparison = scenario_manager.compare(scenario_1, scenario_2, ds_config_name="bar")["bar"]
    assert bar_comparison["subtraction"] == 0

    foo_comparison = scenario_manager.compare(scenario_1, scenario_2, ds_config_name="foo")["foo"]
    assert len(foo_comparison.keys()) == 2
    assert foo_comparison["addition"] == 2
    assert foo_comparison["subtraction"] == 0

    assert len(scenario_manager.compare(scenario_1, scenario_2).keys()) == 2

    with pytest.raises(NonExistingScenarioConfig):
        scenario_manager.compare(scenario_3, scenario_3)

    with pytest.raises(NonExistingComparator):
        scenario_manager.compare(scenario_1, scenario_2, ds_config_name="abc")
