"""Services for Taskman.

author: codecakes
"""
import uuid
from typing import Tuple, List, Type, Any, Callable, Dict

from core.taskman.interface import ITaskQueueRepository
from core.taskman.domain.entity import (
    TaskQueueManagerAggregate,
    Task,
    TaskQueue,
    TaskWorker,
    TaskStatus,
)


class QueuingService:
    """Service for queuing tasks."""

    __slots__ = ("_repo",)

    def __init__(self, queue_repository: Type[ITaskQueueRepository]):
        self._repo = queue_repository

    def register_task_queue(
        self, queue_name: str, num_workers: int
    ) -> Tuple[TaskQueue, List[TaskWorker]]:
        """Registers a task queue alloting workers.

        Provides a callback to start the workers and handle failure.
        """
        task_queue, workers = TaskQueueManagerAggregate.register_queue(
            queue_name, num_workers
        )
        self._repo.create(
            task_queue.queue_name,
            workers=workers,
        )
        return task_queue, workers
        # TODO: Implement this if needed.
        #     .then(
        #     on_success=TaskQueueManagerAggregate.start_workers,
        #     on_failure=TaskQueueManagerAggregate.handle_failure,
        # )

    def submit_task(
        self,
        queue_name: str,
        func_descriptor: Callable[..., Any],
        /,
        *args: Tuple[Any, ...],
        **task_options: Dict[str, Any],
    ) -> Task:
        """Submit a task to a queue."""
        if not (task_queue := self._repo.get(queue_name)):
            raise ValueError(f"Queue {queue_name} does not exist.")
        task: Task = TaskQueueManagerAggregate.create_task(
            task_queue, func_descriptor, *args, **task_options
        )
        self._repo.add_task(
            queue_name,
            task.task_func,
            *task.args,
            task_status=task.status,
            **task.options,
        )
        return task

    # def get_tasks(self, queue_name: str) -> List[Task]:
    #     """Get tasks from a queue."""
    #     if not (task_queue := self._repo.get(queue_name)):
    #         raise ValueError(f"Queue {queue_name} does not exist.")
    #     return task_queue.tasks

    def task_status(
        self, queue_name: str, task_id: uuid.UUID
    ) -> TaskStatus | None:
        """Get task status."""
        if not (task_queue := self._repo.get(queue_name)):
            raise ValueError(f"Queue {queue_name} does not exist.")
        return TaskQueueManagerAggregate.get_task_status(task_queue, task_id)
