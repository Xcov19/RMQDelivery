"""Core TaskQueue domain models."""
import enum
import uuid
from typing import List, Callable, Tuple, Any, Dict

import pydantic


class TaskStatus(enum.Enum):
    ENQUEUED = 1
    PROCESSING = 2
    DONE = 3


class Task(pydantic.BaseModel):
    """A task."""

    task_id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)
    task_func: Callable[..., Any]
    args: Tuple[Any, ...] = pydantic.Field(default_factory=tuple)
    options: Dict[str, Any] = pydantic.Field(default_factory=dict)
    status: TaskStatus = pydantic.Field(default=TaskStatus.ENQUEUED)


class TaskWorker(pydantic.BaseModel):
    """A task worker."""

    worker_name: str
    queues: List[str]


class TaskQueue(pydantic.BaseModel):
    """A task queue."""

    queue_name: str
    num_task_workers: int = 0
    task_workers: List[TaskWorker] = pydantic.Field(default_factory=list)
    tasks: List[Task] = pydantic.Field(default_factory=list)

    def put(self, task: Task) -> None:
        """Enqueue a task."""
        self.tasks += [task]

    def get_task_by_id(self, task_id: uuid.UUID) -> Task | None:
        """Get a task by its ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    @pydantic.validator("tasks", each_item=True)
    @classmethod
    def validate_task(cls, task: Task) -> Task:
        """Validate task."""
        try:
            assert isinstance(task, Task)
        except AssertionError as assert_exc:
            raise ValueError(
                f"Task {task} is not a valid task."
            ) from assert_exc
        return task

    @pydantic.validator("task_workers", each_item=True)
    @classmethod
    def validate_task_workers(cls, task_worker: TaskWorker) -> TaskWorker:
        """Validate task worker."""
        try:
            assert isinstance(task_worker, TaskWorker)
        except AssertionError as assert_exc:
            raise ValueError(
                f"Task worker {task_worker} is not a valid task worker."
            ) from assert_exc
        return task_worker


class TaskQueueManagerAggregate:
    @classmethod
    def register_queue(
        cls, queue_name: str, num_workers: int = 2
    ) -> Tuple[TaskQueue, List[TaskWorker]]:
        """Register a queue."""

        workers = [
            TaskWorker(
                worker_name=cls._name_worker(queue_name, count),
                queues=[queue_name],
            )
            for count in range(num_workers)
        ]
        task_queue = TaskQueue(
            queue_name=queue_name,
            num_task_workers=num_workers,
            task_workers=workers,
        )
        return task_queue, workers

    @classmethod
    def create_task(
        cls,
        task_queue: TaskQueue,
        func_descriptor: Callable[..., Any],
        *args: Tuple[Any, ...],
        **task_kwargs: Dict[str, Any],
    ) -> Task:
        """Create a task."""
        task = Task(
            task_func=func_descriptor,
            args=args,
            **task_kwargs,
        )
        task_queue.put(task)
        return task

    @classmethod
    def _name_worker(cls, queue_name: str, count: int) -> str:
        return f"{queue_name}_worker_{count}"

    @classmethod
    def get_task_status(
        cls, task_queue: TaskQueue, task_id: uuid.UUID
    ) -> TaskStatus | None:
        """Get a task status."""
        if task := task_queue.get_task_by_id(task_id):
            return task.status
        return None
