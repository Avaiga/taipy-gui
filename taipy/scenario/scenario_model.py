import dataclasses
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from taipy.common.alias import CycleId, PipelineId, ScenarioId


@dataclass
class ScenarioModel:
    id: ScenarioId
    name: str
    pipelines: List[PipelineId]
    properties: dict
    master_scenario: bool
    subscribers: List[Dict]
    cycle: Optional[CycleId] = None

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return ScenarioModel(
            id=data["id"],
            name=data["name"],
            pipelines=data["pipelines"],
            properties=data["properties"],
            master_scenario=data["master_scenario"],
            subscribers=data["subscribers"],
            cycle=CycleId(data["cycle"]) if "cycle" in data else None,
        )
