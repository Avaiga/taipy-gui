import logging
from collections import defaultdict

from taipy.common.alias import Dag, TaskId
from taipy.exceptions import NonExistingTask
from taipy.exceptions.pipeline import NonExistingPipeline
from taipy.pipeline.pipeline import Pipeline
from taipy.pipeline.pipeline_model import PipelineModel
from taipy.repository import FileSystemRepository
from taipy.task import TaskManager


class PipelineRepository(FileSystemRepository[PipelineModel, Pipeline]):
    def to_model(self, pipeline: Pipeline) -> PipelineModel:
        source_task_edges = defaultdict(list)
        task_source_edges = defaultdict(list)
        for task in pipeline.tasks.values():
            for predecessor in task.input.values():
                source_task_edges[str(predecessor.id)].append(str(task.id))
            for successor in task.output.values():
                task_source_edges[str(task.id)].append(str(successor.id))
        return PipelineModel(
            pipeline.id,
            pipeline.parent_id,
            pipeline.config_name,
            pipeline.properties,
            Dag(dict(source_task_edges)),
            Dag(dict(task_source_edges)),
        )

    def from_model(self, model: PipelineModel) -> Pipeline:
        try:
            tasks = self.__to_tasks(model.task_source_edges.keys())
            return Pipeline(model.name, model.properties, tasks, model.id, model.parent_id)
        except NonExistingTask as err:
            logging.error(err.message)
            raise err
        except KeyError:
            pipeline_err = NonExistingPipeline(model.id)
            logging.error(pipeline_err.message)
            raise pipeline_err

    @staticmethod
    def __to_tasks(task_ids):
        return [TaskManager().get(TaskId(i)) for i in task_ids]
