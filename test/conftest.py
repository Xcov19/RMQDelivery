from __future__ import annotations

import logging
import random
import uuid
from typing import (
    Any,
    Annotated,
    Generator,
    Callable,
    Tuple,
    Dict,
    Sequence,
    List,
)

import pytest
from pytest import FixtureRequest

from core.taskman.interface import ITaskQueueRepository
from core.taskman.domain.entity import TaskQueue, Task, TaskWorker, TaskStatus
from core.taskman.domain.services import QueuingService

pytest_logger = logging.getLogger(__file__)
pytest_logger.setLevel(logging.INFO)


# ************************************************* #
# Setup pytest anyio fixture.
# The anyio_backend fixture determines the backends
# and their options that tests and fixtures are run with.
# The AnyIO pytest plugin comes with a function scoped
# fixture with this name which runs everything on all supported backends.
# ************************************************* #
@pytest.fixture(
    scope="session",
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
    ],
)
def anyio_backend(request: FixtureRequest) -> Any:
    return request.param


# ************************************************* #
# Setup a fixture caplog for unsuccessful tests.
# You can run pytest -ra -q to see only unsuccessful logs.
# ************************************************* #
@pytest.fixture(scope="function")
def caplogger(caplog: Any) -> Any:
    caplog.set_level(logging.ERROR, logger="test.test_redis_consumer")
    return caplog


# ************************************************* #
# Setup a fixture for the QueuingService.

stub_num_workers = 2


def universal_uuid() -> uuid.UUID:
    """Generate a uuid5 wiht a deterministic seed."""
    random.seed(0)
    return uuid.uuid5(uuid.NAMESPACE_DNS, str(random.random().hex))


def func_descriptor() -> Callable[[List[int]], int]:
    """Return a function with a fixed descriptor."""
    return lambda x_list: sum(x_list)


def stub_args() -> Tuple[int, ...]:
    """Returns stubbed arguments."""
    return 1, 2, 3, 4, 5


@pytest.fixture(scope="function")
def stub_task_param_dict() -> (
    Annotated[
        Dict[str, Any],
        pytest.fixture,
    ]
):
    """Returns a dictionary of stubbed attribtues."""
    return dict(
        task_id=universal_uuid(),
        task_func=func_descriptor,
        args=stub_args(),
        num_workers=stub_num_workers,
    )


class DummyTaskQueueRepo(ITaskQueueRepository):
    """Dummy Task Queue Repository."""

    QueueMockDb: Dict[str, TaskQueue] = {}

    @classmethod
    def create(
        cls,
        queue_name: str,
        /,
        **options: str | Sequence[str] | Sequence[TaskWorker] | Sequence[Task],
    ) -> None:
        """Create a queue."""
        pytest_logger.info("creating queue: %s", queue_name)
        task_queue = TaskQueue(
            queue_name=queue_name,
            num_task_workers=stub_num_workers,
        )
        cls.QueueMockDb[queue_name] = task_queue

    @classmethod
    def add_task(
        cls,
        queue_name: str,
        func_descriptor: Callable[..., Any],
        /,
        *task_args: Tuple[Any, ...],
        task_status: TaskStatus = TaskStatus.ENQUEUED,
        **task_opts: str
        | Sequence[str]
        | Sequence[TaskWorker]
        | Sequence[Task],
    ) -> None:
        if not (task_queue := cls.get(queue_name)):
            raise ValueError(f"Queue {queue_name} does not exist.")
        task_queue.tasks += [
            Task(
                task_id=universal_uuid(),
                task_func=func_descriptor,
                args=task_args,
                status=task_status,
                options=task_opts.get("options", {}),
            )
        ]

    @classmethod
    def get(
        cls,
        queue_name: str,
        /,
        **options: str | Sequence[str] | Sequence[TaskWorker] | Sequence[Task],
    ) -> TaskQueue | None:
        """Get a queue."""
        pytest_logger.info("getting queue: %s", queue_name)
        return cls.QueueMockDb.get(queue_name)

    @classmethod
    def clear(cls) -> None:
        cls.QueueMockDb.clear()


@pytest.fixture(scope="function")
def queue_service() -> (
    Annotated[Generator[QueuingService, None, None], pytest.fixture]
):
    try:
        yield QueuingService(DummyTaskQueueRepo)
    finally:
        DummyTaskQueueRepo.clear()


# ************************************************* #


# ************************************************* #
# Setup redis connection
# ************************************************* #
# @pytest.fixture(scope="function")
# def redis_session(caplogger: pytest.LogCaptureFixture):
#     caplogger.set_level(logging.DEBUG, logger="test.test_redis_consumer")
#     kwargs = {}
#     if redis_pwd := os.getenv("REDIS_PASSWORD", None):
#         kwargs |= dict(password=redis_pwd)
#     pytest_logger.info("starting redis consumer session.")
#     print("starting redis consumer session.")
#     redis_consumer = RedisConsumer(**kwargs)
#     yield redis_consumer
#     pytest_logger.info("closing redis session.")
#     print("closing redis session.")
#     redis_consumer.close()
