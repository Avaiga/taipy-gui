import json
import multiprocessing as mp
import os
import platform
import posixpath
import shutil
import subprocess
import sys
from pathlib import Path
from time import sleep
from typing import Callable, Iterable, List, Optional

import requests  # type: ignore

from taipy.config import Config
from taipy.job import Job
from taipy.scheduler.abstract_scheduler import AbstractScheduler
from taipy.task import Task


class AirflowScheduler(AbstractScheduler):
    """
    Interface with Airflow through API, CLI and disk.

    Dag generation are handle by the `to_dag` script that will convert JSON generated by this class
    to Airflow DAGs. The Config own the target of the disk that will hold JSONs and the convertor.

    Taipy trigger DAGs through the Airflow webserver. The Airflow auth should be set to `basic_auth`
    and the password of the Admin account should be put inside of Airflow Home set in the Config.

    In dev mode, the application can start an Airflow scheduler and webserver thanks to the
    `airflow standalone` command line. Airflow will run in background and the other part of the code
    will stay the same.
    """

    def __init__(self):
        super().__init__()
        self.airflow = None

    def __del__(self):
        self.stop()

    def submit(self, pipeline, callbacks: Optional[Iterable[Callable]] = None) -> List[Job]:
        """Submit pipeline for execution.

        Args:
             pipeline: Pipeline to be transformed into Job(s) for execution.
             callbacks: Optional list of functions that should be executed once the job is done.

        Returns:
            Job created.
        """
        tasks = [task for ts in pipeline.get_sorted_tasks() for task in ts]
        self._do_submit(pipeline.id, tasks)
        return []

    def submit_task(self, task: Task, callbacks: Optional[Iterable[Callable]] = None):
        self._do_submit(task.id, [task])
        return None

    def _do_submit(self, dag_id, tasks: List[Task]) -> List[Job]:
        self.start()
        self.__create_dag(dag_id, tasks)
        self._wait_dag_exists(dag_id)
        self._unpaused(dag_id)
        self._trigger(dag_id)
        return []

    def is_running(self) -> bool:
        """
        Airflow Webserver writes its PID in a file when is it ready.
        Checking if exist allow us to know if Airflow is already running or not.

        Return:
            True if the file exist and so, an Airflow process is running
        """
        pid_file = self.__airflow_folder / "airflow-webserver.pid"

        return pid_file.exists()

    def start(self):
        """
        Init and run Airflow in background and in the `standalone` mode.

        This function check if the file that contains the PID of the Airflow Webserver exists.
        If exists, nothing is done, else we init the Airflow Database then start the Webserver and Scheduler.
        """
        self.__create_airflow_folder()
        self.__add_dag_folder()
        self.__add_json_to_airflow_convertor()

        if not self.is_running() and self.__can_start_airflow():
            self.__start_airflow()

    def stop(self):
        """Stop Airflow process if exists"""
        if self.airflow:
            self.airflow.kill()

    def __start_airflow(self):
        stdout_file = self.__airflow_folder / "stdout"
        stderr_file = self.__airflow_folder / "stderr"

        self.airflow = mp.Process(
            target=self.__start_airflow_in_standalone_mode,
            args=(self.__airflow_folder, self.__dag_folder, stdout_file, stderr_file),
        )
        self.airflow.start()
        self.__retry_on_airflow(self.is_running)

    def __create_dag(self, dag_id, tasks):
        json_model = {
            "path": self.generate_airflow_path(),
            "dag_id": dag_id,
            "storage_folder": self.generate_storage_folder_path(),  # type: ignore
            "tasks": [task.id for task in tasks],
        }
        dag_path = Path(Config.job_config().airflow_dags_folder).resolve() / "taipy" / f"{dag_id}.json"  # type: ignore

        dag_path.write_text(json.dumps(json_model))

    @staticmethod
    def generate_storage_folder_path():
        if platform.system() == "Linux":
            return str(Path(Config.global_config().storage_folder).resolve())
        else:
            linux_storage_mount_path = str(Path(Config.global_config().storage_folder)).replace(os.sep, posixpath.sep)
            linux_storage_mount_path = linux_storage_mount_path.replace(":", "")
            linux_storage_mount_path = linux_storage_mount_path.lower()
            window_path = "/mnt/" + linux_storage_mount_path
            return window_path

    @staticmethod
    def generate_airflow_path():
        if platform.system() == "Linux":
            return sys.path[0]
        else:
            linux_airflow_mount_path = str(Path(sys.path[0])).replace(os.sep, posixpath.sep)
            linux_airflow_mount_path = linux_airflow_mount_path.replace(":", "")
            linux_airflow_mount_path = linux_airflow_mount_path.lower()
            window_airflow_path = "/mnt/" + linux_airflow_mount_path
            return window_airflow_path

    def __create_airflow_folder(self):
        os.makedirs(self.__airflow_folder, exist_ok=True)

    def _wait_dag_exists(self, dag_id: str):
        endpoint = f"{self.__hostname}/api/v1/dags/{dag_id}"
        auth = self.get_credentials()

        dag_exist = self.__retry_on_airflow(lambda: requests.get(endpoint, auth=auth, json=None).status_code == 200)

        if not dag_exist:
            raise RuntimeError(f"Dag {dag_id} doesn't exist")

    def _unpaused(self, dag_id: str):
        requests.patch(
            f"{self.__hostname}/api/v1/dags/{dag_id}", auth=self.get_credentials(), json={"is_paused": False}
        )

    def _trigger(self, dag_id: str):
        requests.post(f"{self.__hostname}/api/v1/dags/{dag_id}/dagRuns", auth=self.get_credentials(), json={})

    def __add_dag_folder(self):
        taipy_dag_folder = self.__dag_folder / "taipy"

        self.__dag_folder.mkdir(exist_ok=True)
        taipy_dag_folder.mkdir(exist_ok=True)

    def __add_json_to_airflow_convertor(self):
        from taipy.scheduler.airflow import to_dag

        shutil.copy(to_dag.__file__, self.__dag_folder)

    @staticmethod
    def __start_airflow_in_standalone_mode(airflow_folder, airflow_dags_folder, stdout_file, stderr_file):
        """
        Start Airflow in the Standalone mode through its CLI interface.
        Stdout and Stderr are redirects in two different files to keep logs and limit the
        pollution on the Taipy output.
        The connection on the Airflow webserver will be through the basic_auth, we set it through the environment.
        """
        os.environ["AIRFLOW_HOME"] = str(airflow_folder)
        os.environ["AIRFLOW__CORE__DAGS_FOLDER"] = str(airflow_dags_folder)
        os.environ["AIRFLOW__CORE__LOAD_EXAMPLES"] = str(False)
        os.environ["AIRFLOW__API__AUTH_BACKEND"] = "airflow.api.auth.backend.basic_auth"

        with open(stdout_file, "w") as stdout, open(stderr_file, "w") as stderr:
            if platform.system() == "Linux":
                subprocess.run(["airflow", "standalone"], stdout=stdout, stderr=stderr)
            elif platform.system() == "Windows":
                subprocess.run(["wsl", "airflow", "standalone"], stdout=stdout, stderr=stderr)

    def get_credentials(self):
        user = Config.job_config().airflow_user
        if Config.job_config().airflow_password:
            password = Config.job_config().airflow_password
        else:
            password_file = self.__airflow_folder / "standalone_admin_password.txt"
            password = password_file.read_text()
        return user, password

    @staticmethod
    def __retry_on_airflow(cb):
        nb_retry = Config.job_config().airflow_api_retry

        for i in range(nb_retry):
            try:
                if cb():
                    return True
            except Exception as e:
                print("Ignoring exception:", e)
            sleep(1)
        return False

    @staticmethod
    def __can_start_airflow() -> bool:
        """True if the configuration allow the application to start Airflow itself"""
        return Config.job_config().start_airflow  # type: ignore

    @property
    def __hostname(self) -> str:
        """Hostname of the Airflow webserver"""
        return Config.job_config().hostname  # type: ignore

    @property
    def __airflow_folder(self) -> Path:
        """Airflow home folder where pid of the webserver is written"""
        return Path(Config.job_config().airflow_folder)  # type: ignore

    @property
    def __dag_folder(self) -> Path:
        """Dag folder where the application will move DAGs and convertor"""

        return Path(Config.job_config().airflow_dags_folder)  # type: ignore
