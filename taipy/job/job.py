__all__ = ["Job"]

from concurrent.futures import Future
from datetime import datetime
from typing import Callable, List

from taipy.common.alias import JobId
from taipy.job.status import Status
from taipy.task.task import Task


def _run_callbacks(fn):
    def __run_callbacks(self):
        fn(self)
        for fct in self._subscribers:
            fct(self)

    return __run_callbacks


class Job:
    """Execution of a Task.

    A Job is the execution wrapper around a Task. It handles the status of the execution,
    contains raising exceptions during the execution and notifies subscriber when the job is
    finished.

    Attributes:
        id: Id of the Job.
        task: Task that is executed by the job.
        status: Current status of the job.
        creation_date: Date of the object creation.
    """

    def __init__(self, id: JobId, task: Task):
        self.id = id
        self.task = task
        self.status = Status.SUBMITTED
        self.creation_date = datetime.now()
        self._subscribers: List[Callable] = []
        self.__exceptions: List[Exception] = []

    def __contains__(self, task: Task):
        """Allows to know if the Job contains a specific task.

        Returns:
            True if the Job is based on this task.
        """
        return self.task.id == task.id

    def __lt__(self, other):
        return self.creation_date.timestamp() < other.creation_date.timestamp()

    def __le__(self, other):
        return self.creation_date.timestamp() == other.creation_date.timestamp() or self < other

    def __gt__(self, other):
        return self.creation_date.timestamp() > other.creation_date.timestamp()

    def __ge__(self, other):
        return self.creation_date.timestamp() == other.creation_date.timestamp() or self > other

    def __eq__(self, other):
        return self.id == other.id

    @property
    def exceptions(self) -> List[Exception]:
        """Contains exceptions raised during the execution.

        Returns:
            Exceptions raised as list.
        """
        return self.__exceptions

    @_run_callbacks
    def blocked(self):
        """Sets the status to blocked and notifies subscribers."""
        self.status = Status.BLOCKED

    @_run_callbacks
    def pending(self):
        """Sets the status to pending and notifies subscribers."""
        self.status = Status.PENDING

    @_run_callbacks
    def running(self):
        """Sets the status to running and notifies subscribers."""
        self.status = Status.RUNNING

    @_run_callbacks
    def cancelled(self):
        """Sets the status to cancelled and notifies subscribers."""
        self.status = Status.CANCELLED

    @_run_callbacks
    def failed(self):
        """Sets the status to failed and notifies subscribers."""
        self.status = Status.FAILED

    @_run_callbacks
    def completed(self):
        """Sets the status to completed and notifies subscribers."""
        self.status = Status.COMPLETED

    def is_failed(self) -> bool:
        """Allows to know if the job failed.

        Returns:
            True if the job has failed.
        """
        return self.status == Status.FAILED

    def is_blocked(self) -> bool:
        """Allows to know if the job is blocked.

        Returns:
            True if the job is blocked.
        """
        return self.status == Status.BLOCKED

    def is_cancelled(self) -> bool:
        """Allows to know if the job is cancelled.

        Returns:
            True if the job is cancelled.
        """
        return self.status == Status.CANCELLED

    def is_submitted(self) -> bool:
        """Allows to know if the job is submitted.

        Returns:
            True if the job is submitted.
        """
        return self.status == Status.SUBMITTED

    def is_completed(self) -> bool:
        """Allows to know if the job is completed.

        Returns:
            True if the job is completed.
        """
        return self.status == Status.COMPLETED

    def is_running(self) -> bool:
        """Allows to know if the job is running.

        Returns:
            True if the job is running.
        """
        return self.status == Status.RUNNING

    def is_pending(self) -> bool:
        """Allows to know if the job is pending.

        Returns:
            True if the job is pending.
        """
        return self.status == Status.PENDING

    def is_finished(self) -> bool:
        """Allows to know if the job is finished.

        Returns:
            True if the job is finished.
        """
        return self.is_completed() or self.is_failed() or self.is_cancelled()

    def on_status_change(self, *functions):
        """Allows to be notified when the status of the job changes.

        Job passing through multiple statuses (Submitted, pending, etc.) before being finished.
        You can be triggered on each change through this function unless for the `Submitted` status.

        Args:
            functions: Callables that will be called on each status change.
        """
        functions = list(functions)
        function = functions.pop()
        self._subscribers.append(function)

        if self.status != Status.SUBMITTED:
            function(self)

        if functions:
            self.on_status_change(*functions)

    def update_status(self, ft: Future):
        """Update the Job status based on if an exception was raised or not."""
        self.__exceptions = ft.result()
        if self.__exceptions:
            self.failed()
        else:
            self.completed()
