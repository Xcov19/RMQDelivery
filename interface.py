import abc
from typing import Protocol, Optional, TypeVar


t_consumer_id = TypeVar('consumer_id', bound=str)


class Consumer(Protocol):
  """This class consumes input.
  Each consumer entry creates a dedicated channel to consume into.
  """

  @abc.abstractmethod
  def setup(self, channel: Optional[str] = None, **kwargs) -> t_consumer_id:
    """Setup the consumer."""
    raise NotImplementedError
  
  @abc.abstractmethod
  def consume(self, data: dict, **optional_attrs) -> None:
    """Consume input."""
    raises NotImplementedError


class Producer(Protocol):
  """This class produces output.
  
  Each producer entry publishes from a dedicated channel.
  """

  @abc.abstractmethod
  def setup(self, consumer_id: t_consumer_id, **kwargs) -> None:
    """Setup the producer."""
    raise NotImplementedError

  @abc.abstractmethod
  def get(self, **optional_attrs) -> None:
    """Returns output."""
    raise NotImplementedError
  