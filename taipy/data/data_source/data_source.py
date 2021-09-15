from taipy.data.data_source.models import Scope


class DataSource:

    def __init__(self, name: str, type: str, scope=Scope.PIPELINE, **kwargs):
        self.type = type
        self.name = name
        self.scope = scope
        self.properties = kwargs
