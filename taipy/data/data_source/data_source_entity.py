import uuid
from abc import abstractmethod
from typing import Optional

from taipy.data.data_source.models import Scope


class DataSourceEntity:
    """
    A class to represent a Data Source. A Data Source is an object that holds the name, scope and additional
    properties of the data source.

    Attributes
    ----------
    id: str
        unique identifier of the data source
    name: str
        name that identifies the data source
    scope: int
        number that refers to the scope of usage of the data source
    properties: list
        list of additional arguments
    """

    def __init__(
        self, name, scope: Scope = Scope.PIPELINE, id: Optional[str] = None, **kwargs
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.scope = scope
        self.properties = kwargs

    @classmethod
    @abstractmethod
    def type(cls) -> str:
        return NotImplemented

    @abstractmethod
    def preview(self):
        return NotImplemented

    @abstractmethod
    def get(self, query=None):
        return NotImplemented

    @abstractmethod
    def write(self, data):
        """
        Temporary function interface, will be remove
        """
        return NotImplemented

    def to_json(self):
        pass

    def from_json(self):
        pass
