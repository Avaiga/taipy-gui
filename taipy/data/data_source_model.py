from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dataclasses_json import dataclass_json

from taipy.common.alias import JobId
from taipy.data.scope import Scope


@dataclass_json
@dataclass
class DataSourceModel:
    """
    The model of a DataSource.
    
    A model refers to the structure of a Data Source stored in a database.

    Attributes:
        id (str): Identifier of a DataSource.
        config_name (int): Name of the `DataSourceConfig`.
        scope (taipy.data.source.scope.Scope): Scope of the usage of a DataSource.
        type (str):  Name of the class that represents a DataSource.
        name (str): User-readable name of the data source.
        parent_id (str): Identifier of the parent (pipeline_id, scenario_id, cycle_id) or `None`.
        last_computation_date (str): ISO format of the last computation date and time.
        job_ids (List[str]): List of jobs that computed the data source.
        data_source_properties (Dict[str, Any]): Additional properties of the data source.

    Note:
        The tuple `(config_name, parent_id)` forms a unique key.
    """

    id: str
    config_name: str
    scope: Scope
    type: str
    name: str
    parent_id: Optional[str]
    last_edition_date: Optional[str]
    job_ids: List[JobId]
    up_to_date: bool
    data_source_properties: Dict[str, Any]
