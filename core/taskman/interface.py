"""Dependency Inversion for redis like queue and stream/pubsub protocols."""
import abc
from typing import Protocol, Dict, Any, Sequence, Callable, Tuple

from core.taskman.domain.entity import Task, TaskQueue, TaskWorker, TaskStatus
from core.utils.types import ChannelableType, ConsumerIdType


class ITaskQueueRepository(Protocol):
    """Task Queue Repository Interface."""

    @classmethod
    @abc.abstractmethod
    def create(
        cls,
        queue_name: str,
        /,
        **options: str | Sequence[str] | Sequence[TaskWorker] | Sequence[Task],
    ) -> None:
        """Create a queue."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def get(
        cls,
        queue_name: str,
        /,
        **options: str | Sequence[str] | Sequence[TaskWorker] | Sequence[Task],
    ) -> TaskQueue | None:
        """Get a queue."""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
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
        """Submit task to a queue."""
        raise NotImplementedError


class IConsumer(Protocol):
    """This class consumes input.

    Each consumer entry creates a dedicated channel to consume into.

    A channel is a `channelable` queue that is bound to an exchange.
    The exchange is defined by the consumer and the queue is defined
    by the channel.
    """

    @abc.abstractmethod
    def setup(
        self, channel: ChannelableType | None = None, **kwargs: Dict[str, Any]
    ) -> str:
        """Set up the consumer."""
        raise NotImplementedError

    @abc.abstractmethod
    def consume(
        self,
        consumer_id: ConsumerIdType,
        data: Dict[str, Any],
        **optional_attrs: Dict[str, Any],
    ) -> None:
        """Consume input."""
        raise NotImplementedError


class IProducer(Protocol):
    """This class produces output.

    Each producer entry publishes from a dedicated channel.
    """

    @abc.abstractmethod
    def setup(self, **kwargs: str) -> ChannelableType:
        """Set up the producer."""
        raise NotImplementedError

    @abc.abstractmethod
    def send(
        self, data: Dict[str, Any], **optional_attrs: Dict[str, Any]
    ) -> None:
        """Send output."""
        raise NotImplementedError
