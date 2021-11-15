import pytest

from taipy.data.in_memory import InMemoryDataSource
from taipy.data.scope import Scope
from taipy.exceptions.data_source import NoData


class TestInMemoryDataSourceEntity:
    def test_create(self):
        ds = InMemoryDataSource(
            "foobar BaZ",
            Scope.SCENARIO,
            "id",
            "my name",
            "parent_id",
            properties={"default_data": "In memory Data Source"},
        )
        assert isinstance(ds, InMemoryDataSource)
        assert ds.type() == "in_memory"
        assert ds.config_name == "foobar_baz"
        assert ds.scope == Scope.SCENARIO
        assert ds.id == "id"
        assert ds.name == "my name"
        assert ds.parent_id == "parent_id"
        assert ds.last_edition_date is not None
        assert ds.job_ids == []
        assert ds.up_to_date
        assert ds.read() == "In memory Data Source"
        assert ds.default_data == "In memory Data Source"

        ds_2 = InMemoryDataSource("foo", Scope.PIPELINE)
        assert ds_2.last_edition_date is None
        assert not ds_2.up_to_date

    def test_read_and_write(self):
        no_data_ds = InMemoryDataSource("foo", Scope.PIPELINE, "ds_id")
        with pytest.raises(NoData):
            no_data_ds.read()
        in_mem_ds = InMemoryDataSource("foo", Scope.PIPELINE, properties={"default_data": "bar"})
        assert isinstance(in_mem_ds.read(), str)
        assert in_mem_ds.read() == "bar"
        in_mem_ds.properties["default_data"] = "baz"  # this modifies the default data value but not the data itself
        assert in_mem_ds.read() == "bar"
        in_mem_ds.write("qux")
        assert in_mem_ds.read() == "qux"
        in_mem_ds.write(1998)
        assert isinstance(in_mem_ds.read(), int)
        assert in_mem_ds.read() == 1998
