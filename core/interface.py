"""Dependency Inversion for redis like queue and stream/pubsub protocols."""
import abc
from typing import Protocol, Optional, TypeVar, NewType

type_consumer_id = TypeVar("type_consumer_id", bound=str)


class ChannelableType(str):
    ...


Channelable = NewType("Channelable", ChannelableType)


class IConsumer(Protocol):
    """This class consumes input.

    Each consumer entry creates a dedicated channel to consume into.

    A channel is a `channelable` queue that is bound to an exchange. The exchange is
    defined by the consumer and the queue is defined by the channel.
    """

    @abc.abstractmethod
    def setup(
        self, channel: Optional[Channelable] = None, **kwargs
    ) -> type_consumer_id:
        """Set up the consumer."""
        raise NotImplementedError

    @abc.abstractmethod
    def consume(self, consumer_id: type_consumer_id, data: dict, **optional_attrs) -> None:
        """Consume input."""
        raise NotImplementedError


class IProducer(Protocol):
    """This class produces output.

    Each producer entry publishes from a dedicated channel.
    """

    @abc.abstractmethod
    def setup(self, consumer_id: type_consumer_id, **kwargs) -> None:
        """Set up the producer."""
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, **optional_attrs) -> None:
        """Returns output."""
        raise NotImplementedError
