"""
Dag convertor from Taipy JSON to Airflow DAGs.

This file should be put inside of the Airflow DAG folder. It convert all JSON from ./taipy" folder.
"""
import json
import sys
from datetime import datetime
from importlib import util
from pathlib import Path
from typing import Dict

from taipy.config import Config
from taipy.task.manager import TaskManager

# This file can be import from Taipy to be moved inside of the Airflow DAG folder.
# Taipy doesn't need any package of Airflow to be able to run, so this import will failed.
if util.find_spec("airflow"):
    from airflow import DAG
    from airflow.operators.python import PythonOperator


def submit(application_path, task_id, storage_folder):
    """
    Execute the Taipy task on Airflow.
    """
    sys.path.insert(0, application_path)
    Config.set_global_config(storage_folder=storage_folder)
    task_manager = TaskManager()
    task = task_manager.get(task_id)
    task_manager.scheduler.submit_task(task)


def to_dag(conf: Dict):
    """
    Generate the Airflow DAGs based on the parameters provide.

    Taipy tasks are converted into two Airflow Operator:
    1) A sensor that will be triggered intermediately and check if task's data nodes are ready.
    2) A operator that will execute the task itself.
    """
    dag = DAG(dag_id=conf["dag_id"], schedule_interval=None)

    kwargs = {
        "storage_folder": conf["storage_folder"],
        "application_path": conf["path"],
    }

    for task_id in conf["tasks"]:
        kwargs = {**kwargs, "task_id": task_id}

        PythonOperator(
            task_id=task_id,
            python_callable=submit,
            dag=dag,
            start_date=datetime(2021, 1, 1),
            op_kwargs=kwargs,
        )
    return dag


dag_folder = Path(__file__)
dag_folder = Path(str(dag_folder.resolve())[: -len(dag_folder.name)]) / "taipy"
for dag_file in dag_folder.glob("*.json"):
    globals()[str(dag_file)] = to_dag(json.loads(dag_file.read_text()))
