"""Dynamic queueing.

author: codecakes
"""
import uuid
from typing import Dict, Callable, Annotated, Tuple, List

import pytest

from core.taskman.domain.entity import Task, TaskStatus
from core.taskman.domain.services import QueuingService


class TestRegisterQueueUsingQueuingService:
    """Test that a queue is created."""

    def test_queue_registered_has_n_workers(
        self, queue_service: QueuingService
    ) -> None:
        """Test that queues are registered"""
        num_workers = 2
        task_queue, workers = queue_service.register_task_queue(
            "test_queue", num_workers
        )
        assert (
            len(workers) == num_workers
        ), f"Expected task queue {task_queue} to have {num_workers} workers."

    def test_enqueue_items_to_queue(
        self,
        queue_service: QueuingService,
        stub_task_param_dict: Annotated[
            Dict[str, uuid.UUID | Callable[[List[int]], int] | Tuple[int]],
            pytest.fixture,
        ],
    ) -> None:
        """Test that items are enqueued to the correct queue."""
        (
            universal_uuid,
            func_descriptor,
            stub_args,
            stub_num_workers,
        ) = stub_task_param_dict.values()

        assert isinstance(stub_num_workers, int)
        task_queue, _workers = queue_service.register_task_queue(
            "test_queue", stub_num_workers
        )
        task: Task | None = queue_service.submit_task(
            "test_queue", func_descriptor, *stub_args, task_id=universal_uuid
        )
        assert isinstance(task, Task) and (
            queue_service.task_status("test_queue", task.task_id)
            == TaskStatus.ENQUEUED
        ), f"Expected task {task} to be enqueued in tasks {task_queue.tasks}."


@pytest.mark.skip(reason="Not implemented")
class TestDynamicWorkerAllocationUsingQueuingService:
    """Test that workers are allocated dynamically."""

    def test_num_workers_dynamically_register_queues(self) -> None:
        """Test that workers can dynamically register queues."""
        assert False
