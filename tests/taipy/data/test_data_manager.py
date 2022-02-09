import os
import pathlib

import pytest

from taipy.common.alias import DataNodeId
from taipy.config.config import Config
from taipy.config.data_node_config import DataNodeConfig
from taipy.data.csv import CSVDataNode
from taipy.data.data_manager import DataManager
from taipy.data.in_memory import InMemoryDataNode
from taipy.data.pickle import PickleDataNode
from taipy.data.scope import Scope
from taipy.exceptions import InvalidDataNodeType, ModelNotFound
from taipy.exceptions.data_node import NonExistingDataNode


class TestDataManager:
    def test_create_data_node_and_modify_properties_does_not_modify_config(self):
        dm = DataManager()
        ds_config = Config.add_data_node(name="name", foo="bar")
        ds = dm._create_and_set(ds_config, None)
        assert ds_config.properties.get("foo") == "bar"
        assert ds_config.properties.get("baz") is None

        ds.properties["baz"] = "qux"
        assert ds_config.properties.get("foo") == "bar"
        assert ds_config.properties.get("baz") is None
        assert ds.properties.get("foo") == "bar"
        assert ds.properties.get("baz") == "qux"

    def test_create_and_get_csv_data_node(self):
        dm = DataManager()
        # Test we can instantiate a CsvDataNode from DataNodeConfig with :
        # - a csv type
        # - a default pipeline scope
        # - No parent_id
        csv_ds_config = Config.add_data_node(name="foo", storage_type="csv", path="bar", has_header=True)
        csv_ds = dm._create_and_set(csv_ds_config, None)

        assert isinstance(csv_ds, CSVDataNode)
        assert isinstance(dm.get(csv_ds.id), CSVDataNode)

        assert dm.get(csv_ds.id) is not None
        assert dm.get(csv_ds.id).id == csv_ds.id
        assert dm.get(csv_ds.id).config_name == "foo"
        assert dm.get(csv_ds.id).config_name == csv_ds.config_name
        assert dm.get(csv_ds.id).scope == Scope.PIPELINE
        assert dm.get(csv_ds.id).scope == csv_ds.scope
        assert dm.get(csv_ds.id).parent_id is None
        assert dm.get(csv_ds.id).parent_id == csv_ds.parent_id
        assert dm.get(csv_ds.id).last_edition_date is None
        assert dm.get(csv_ds.id).last_edition_date == csv_ds.last_edition_date
        assert dm.get(csv_ds.id).job_ids == []
        assert dm.get(csv_ds.id).job_ids == csv_ds.job_ids
        assert not dm.get(csv_ds.id).is_ready_for_reading
        assert dm.get(csv_ds.id).is_ready_for_reading == csv_ds.is_ready_for_reading
        assert len(dm.get(csv_ds.id).properties) == 2
        assert dm.get(csv_ds.id).properties.get("path") == "bar"
        assert dm.get(csv_ds.id).properties.get("has_header")
        assert dm.get(csv_ds.id).properties == csv_ds.properties

        assert dm.get(csv_ds) is not None
        assert dm.get(csv_ds).id == csv_ds.id
        assert dm.get(csv_ds).config_name == "foo"
        assert dm.get(csv_ds).config_name == csv_ds.config_name
        assert dm.get(csv_ds).scope == Scope.PIPELINE
        assert dm.get(csv_ds).scope == csv_ds.scope
        assert dm.get(csv_ds).parent_id is None
        assert dm.get(csv_ds).parent_id == csv_ds.parent_id
        assert dm.get(csv_ds).last_edition_date is None
        assert dm.get(csv_ds).last_edition_date == csv_ds.last_edition_date
        assert dm.get(csv_ds).job_ids == []
        assert dm.get(csv_ds).job_ids == csv_ds.job_ids
        assert not dm.get(csv_ds).is_ready_for_reading
        assert dm.get(csv_ds).is_ready_for_reading == csv_ds.is_ready_for_reading
        assert len(dm.get(csv_ds).properties) == 2
        assert dm.get(csv_ds).properties.get("path") == "bar"
        assert dm.get(csv_ds).properties.get("has_header")
        assert dm.get(csv_ds).properties == csv_ds.properties

    def test_create_and_get_in_memory_data_node(self):
        dm = DataManager()
        # Test we can instantiate an InMemoryDataNode from DataNodeConfig with :
        # - an in_memory type
        # - a scenario scope
        # - a parent id
        # - some default data
        in_memory_ds_config = Config.add_data_node(
            name="baz", storage_type="in_memory", scope=Scope.SCENARIO, default_data="qux"
        )
        in_mem_ds = dm._create_and_set(in_memory_ds_config, "Scenario_id")

        assert isinstance(in_mem_ds, InMemoryDataNode)
        assert isinstance(dm.get(in_mem_ds.id), InMemoryDataNode)

        assert dm.get(in_mem_ds.id) is not None
        assert dm.get(in_mem_ds.id).id == in_mem_ds.id
        assert dm.get(in_mem_ds.id).config_name == "baz"
        assert dm.get(in_mem_ds.id).config_name == in_mem_ds.config_name
        assert dm.get(in_mem_ds.id).scope == Scope.SCENARIO
        assert dm.get(in_mem_ds.id).scope == in_mem_ds.scope
        assert dm.get(in_mem_ds.id).parent_id == "Scenario_id"
        assert dm.get(in_mem_ds.id).parent_id == in_mem_ds.parent_id
        assert dm.get(in_mem_ds.id).last_edition_date is not None
        assert dm.get(in_mem_ds.id).last_edition_date == in_mem_ds.last_edition_date
        assert dm.get(in_mem_ds.id).job_ids == []
        assert dm.get(in_mem_ds.id).job_ids == in_mem_ds.job_ids
        assert dm.get(in_mem_ds.id).is_ready_for_reading
        assert dm.get(in_mem_ds.id).is_ready_for_reading == in_mem_ds.is_ready_for_reading
        assert len(dm.get(in_mem_ds.id).properties) == 1
        assert dm.get(in_mem_ds.id).properties.get("default_data") == "qux"
        assert dm.get(in_mem_ds.id).properties == in_mem_ds.properties

        assert dm.get(in_mem_ds) is not None
        assert dm.get(in_mem_ds).id == in_mem_ds.id
        assert dm.get(in_mem_ds).config_name == "baz"
        assert dm.get(in_mem_ds).config_name == in_mem_ds.config_name
        assert dm.get(in_mem_ds).scope == Scope.SCENARIO
        assert dm.get(in_mem_ds).scope == in_mem_ds.scope
        assert dm.get(in_mem_ds).parent_id == "Scenario_id"
        assert dm.get(in_mem_ds).parent_id == in_mem_ds.parent_id
        assert dm.get(in_mem_ds).last_edition_date is not None
        assert dm.get(in_mem_ds).last_edition_date == in_mem_ds.last_edition_date
        assert dm.get(in_mem_ds).job_ids == []
        assert dm.get(in_mem_ds).job_ids == in_mem_ds.job_ids
        assert dm.get(in_mem_ds).is_ready_for_reading
        assert dm.get(in_mem_ds).is_ready_for_reading == in_mem_ds.is_ready_for_reading
        assert len(dm.get(in_mem_ds).properties) == 1
        assert dm.get(in_mem_ds).properties.get("default_data") == "qux"
        assert dm.get(in_mem_ds).properties == in_mem_ds.properties

    def test_create_and_get_pickle_data_node(self):
        dm = DataManager()
        # Test we can instantiate a PickleDataNode from DataNodeConfig with :
        # - an in_memory type
        # - a business cycle scope
        # - No parent id
        # - no default data
        ds_config = Config.add_data_node(name="plop", storage_type="pickle", scope=Scope.BUSINESS_CYCLE)
        pickle_ds = dm._create_and_set(ds_config, None)

        assert isinstance(pickle_ds, PickleDataNode)
        assert isinstance(dm.get(pickle_ds.id), PickleDataNode)

        assert dm.get(pickle_ds.id) is not None
        assert dm.get(pickle_ds.id).id == pickle_ds.id
        assert dm.get(pickle_ds.id).config_name == "plop"
        assert dm.get(pickle_ds.id).config_name == pickle_ds.config_name
        assert dm.get(pickle_ds.id).scope == Scope.BUSINESS_CYCLE
        assert dm.get(pickle_ds.id).scope == pickle_ds.scope
        assert dm.get(pickle_ds.id).parent_id is None
        assert dm.get(pickle_ds.id).parent_id == pickle_ds.parent_id
        assert dm.get(pickle_ds.id).last_edition_date is None
        assert dm.get(pickle_ds.id).last_edition_date == pickle_ds.last_edition_date
        assert dm.get(pickle_ds.id).job_ids == []
        assert dm.get(pickle_ds.id).job_ids == pickle_ds.job_ids
        assert not dm.get(pickle_ds.id).is_ready_for_reading
        assert dm.get(pickle_ds.id).is_ready_for_reading == pickle_ds.is_ready_for_reading
        assert len(dm.get(pickle_ds.id).properties) == 0
        assert dm.get(pickle_ds.id).properties == pickle_ds.properties

        assert dm.get(pickle_ds) is not None
        assert dm.get(pickle_ds).id == pickle_ds.id
        assert dm.get(pickle_ds).config_name == "plop"
        assert dm.get(pickle_ds).config_name == pickle_ds.config_name
        assert dm.get(pickle_ds).scope == Scope.BUSINESS_CYCLE
        assert dm.get(pickle_ds).scope == pickle_ds.scope
        assert dm.get(pickle_ds).parent_id is None
        assert dm.get(pickle_ds).parent_id == pickle_ds.parent_id
        assert dm.get(pickle_ds).last_edition_date is None
        assert dm.get(pickle_ds).last_edition_date == pickle_ds.last_edition_date
        assert dm.get(pickle_ds).job_ids == []
        assert dm.get(pickle_ds).job_ids == pickle_ds.job_ids
        assert not dm.get(pickle_ds).is_ready_for_reading
        assert dm.get(pickle_ds).is_ready_for_reading == pickle_ds.is_ready_for_reading
        assert len(dm.get(pickle_ds).properties) == 0
        assert dm.get(pickle_ds).properties == pickle_ds.properties

    def test_create_raises_exception_with_wrong_type(self):
        dm = DataManager()
        wrong_type_ds_config = DataNodeConfig(name="foo", storage_type="bar", scope=DataNodeConfig.DEFAULT_SCOPE)
        with pytest.raises(InvalidDataNodeType):
            dm._create_and_set(wrong_type_ds_config, None)

    def test_create_from_same_config_generates_new_data_node_and_new_id(self):
        dm = DataManager()
        ds_config = Config.add_data_node(name="foo", storage_type="in_memory")
        ds = dm._create_and_set(ds_config, None)
        ds_2 = dm._create_and_set(ds_config, None)
        assert ds_2.id != ds.id

    def test_create_uses_overridden_attributes_in_config_file(self):
        Config.load(os.path.join(pathlib.Path(__file__).parent.resolve(), "data_sample/config.toml"))

        dm = DataManager()
        csv_ds = Config.add_data_node(name="foo", storage_type="csv", path="bar", has_header=True)
        csv = dm._create_and_set(csv_ds, None)
        assert csv.config_name == "foo"
        assert isinstance(csv, CSVDataNode)
        assert csv.path == "path_from_config_file"
        assert csv.has_header

        csv_ds = Config.add_data_node(name="baz", storage_type="csv", path="bar", has_header=True)
        csv = dm._create_and_set(csv_ds, None)
        assert csv.config_name == "baz"
        assert isinstance(csv, CSVDataNode)
        assert csv.path == "bar"
        assert csv.has_header

    def test_get_if_not_exists(self):
        with pytest.raises(ModelNotFound):
            DataManager().repository.load("test_data_node_2")

    def test_get_all(self):
        dm = DataManager()
        assert len(dm.get_all()) == 0
        ds_config_1 = Config.add_data_node(name="foo", storage_type="in_memory")
        dm._create_and_set(ds_config_1, None)
        assert len(dm.get_all()) == 1
        ds_config_2 = Config.add_data_node(name="baz", storage_type="in_memory")
        dm._create_and_set(ds_config_2, None)
        dm._create_and_set(ds_config_2, None)
        assert len(dm.get_all()) == 3
        assert len([ds for ds in dm.get_all() if ds.config_name == "foo"]) == 1
        assert len([ds for ds in dm.get_all() if ds.config_name == "baz"]) == 2

    def test_get_all_by_config_name(self):
        dm = DataManager()
        assert len(dm._get_all_by_config_name("NOT_EXISTING_CONFIG_NAME")) == 0
        ds_config_1 = Config.add_data_node(name="foo", storage_type="in_memory")
        assert len(dm._get_all_by_config_name("foo")) == 0
        dm._create_and_set(ds_config_1, None)
        assert len(dm._get_all_by_config_name("foo")) == 1
        ds_config_2 = Config.add_data_node(name="baz", storage_type="in_memory")
        dm._create_and_set(ds_config_2, None)
        assert len(dm._get_all_by_config_name("foo")) == 1
        assert len(dm._get_all_by_config_name("baz")) == 1
        dm._create_and_set(ds_config_2, None)
        assert len(dm._get_all_by_config_name("foo")) == 1
        assert len(dm._get_all_by_config_name("baz")) == 2

    def test_set(self):
        dm = DataManager()
        ds = InMemoryDataNode(
            "config_name",
            Scope.PIPELINE,
            id=DataNodeId("id"),
            parent_id=None,
            last_edition_date=None,
            job_ids=[],
            edition_in_progress=False,
            properties={"foo": "bar"},
        )
        assert len(dm.get_all()) == 0
        dm.set(ds)
        assert len(dm.get_all()) == 1

        # changing data node attribute
        ds.config_name = "foo"
        assert ds.config_name == "foo"
        assert dm.get(ds.id).config_name == "config_name"
        dm.set(ds)
        assert len(dm.get_all()) == 1
        assert ds.config_name == "foo"
        assert dm.get(ds.id).config_name == "foo"

    def test_delete(self):
        dm = DataManager()
        ds_1 = InMemoryDataNode("config_name", Scope.PIPELINE, id="id_1")
        ds_2 = InMemoryDataNode("config_name", Scope.PIPELINE, id="id_2")
        ds_3 = InMemoryDataNode("config_name", Scope.PIPELINE, id="id_3")
        assert len(dm.get_all()) == 0
        dm.set(ds_1)
        dm.set(ds_2)
        dm.set(ds_3)
        assert len(dm.get_all()) == 3
        dm.delete(ds_1.id)
        assert len(dm.get_all()) == 2
        assert dm.get(ds_2.id).id == ds_2.id
        assert dm.get(ds_3.id).id == ds_3.id
        with pytest.raises(NonExistingDataNode):
            dm.get(ds_1.id)
        dm.delete_all()
        assert len(dm.get_all()) == 0

    def test_get_or_create(self):
        dm = DataManager()
        dm.delete_all()

        global_ds_config = Config.add_data_node(
            name="test_data_node", storage_type="in_memory", scope=Scope.GLOBAL, data="In memory Data Node"
        )
        scenario_ds_config = Config.add_data_node(
            name="test_data_node2", storage_type="in_memory", scope=Scope.SCENARIO, data="In memory scenario"
        )
        pipeline_ds_config = Config.add_data_node(
            name="test_data_node2", storage_type="in_memory", scope=Scope.PIPELINE, data="In memory pipeline"
        )

        assert len(dm.get_all()) == 0
        global_ds = dm.get_or_create(global_ds_config, None, None)
        assert len(dm.get_all()) == 1
        global_ds_bis = dm.get_or_create(global_ds_config, None)
        assert len(dm.get_all()) == 1
        assert global_ds.id == global_ds_bis.id

        scenario_ds = dm.get_or_create(scenario_ds_config, "scenario_id")
        assert len(dm.get_all()) == 2
        scenario_ds_bis = dm.get_or_create(scenario_ds_config, "scenario_id")
        assert len(dm.get_all()) == 2
        assert scenario_ds.id == scenario_ds_bis.id
        scenario_ds_ter = dm.get_or_create(scenario_ds_config, "scenario_id", "whatever_pipeline_id")
        assert len(dm.get_all()) == 2
        assert scenario_ds.id == scenario_ds_bis.id
        assert scenario_ds_bis.id == scenario_ds_ter.id
        scenario_ds_quater = dm.get_or_create(scenario_ds_config, "scenario_id_2")
        assert len(dm.get_all()) == 3
        assert scenario_ds.id == scenario_ds_bis.id
        assert scenario_ds_bis.id == scenario_ds_ter.id
        assert scenario_ds_ter.id != scenario_ds_quater.id

        pipeline_ds = dm.get_or_create(pipeline_ds_config, "scenario_id", "pipeline_1")
        assert len(dm.get_all()) == 4
        pipeline_ds_bis = dm.get_or_create(pipeline_ds_config, "scenario_id", "pipeline_1")
        assert len(dm.get_all()) == 4
        assert pipeline_ds.id == pipeline_ds_bis.id
        pipeline_ds_ter = dm.get_or_create(pipeline_ds_config, "scenario_id", "pipeline_2")
        assert len(dm.get_all()) == 5
        assert pipeline_ds.id == pipeline_ds_bis.id
        assert pipeline_ds.id != pipeline_ds_ter.id
        pipeline_ds_quater = dm.get_or_create(pipeline_ds_config, "other_scenario_id", "pipeline_2")
        assert len(dm.get_all()) == 5
        assert pipeline_ds.id == pipeline_ds_bis.id
        assert pipeline_ds_bis.id != pipeline_ds_ter.id
        assert pipeline_ds_ter.id == pipeline_ds_quater.id

        pipeline_ds_config.name = "test_data_node4"
        pipeline_ds_quinquies = dm.get_or_create(pipeline_ds_config, None)
        assert len(dm.get_all()) == 6
        assert pipeline_ds.id == pipeline_ds_bis.id
        assert pipeline_ds_bis.id != pipeline_ds_ter.id
        assert pipeline_ds_bis.id != pipeline_ds_quinquies.id
        assert pipeline_ds_ter.id != pipeline_ds_quinquies.id

    def test_ensure_persistence_of_data_node(self):
        dm = DataManager()
        dm.delete_all()

        ds_config_1 = Config.add_data_node(name="data node 1", storage_type="in_memory", data="In memory pipeline 2")
        ds_config_2 = Config.add_data_node(name="data node 2", storage_type="in_memory", data="In memory pipeline 2")

        # Create and save
        dm.get_or_create(ds_config_1)
        dm.get_or_create(ds_config_2)
        assert len(dm.get_all()) == 2

        # Delete the DataManager to ensure it's get from the storage system
        del dm
        dm = DataManager()
        dm.get_or_create(ds_config_1)
        assert len(dm.get_all()) == 2

        dm.delete_all()
