from __future__ import annotations

import functools
import uuid
from typing import TypeVar, Tuple, Any, Callable, NewType, Optional, Dict

import pydantic
from redis_om import JsonModel, Field


class Channelable(JsonModel):  # type: ignore
    id: uuid.UUID
    name: str = Field(index=True)


class Thenable:
    """A monadic encapsulation that chains results and exception."""

    def __init__(self, *result: Tuple[Optional[Any], Optional[Any]]):
        if not result:
            raise TypeError("No result")
        if not len(result) == 2:
            raise TypeError(
                (
                    "Thenable result should have {success_result, failure_result}."
                    f" Is of size: {len(result)}."
                )
            )
        self._result = result

    def then(
        self,
        on_success: Callable[..., Any],
        on_failure: Callable[..., Any],
    ) -> Thenable:
        success_result, failure_result = self._result
        if failure_result:
            return Thenable((None, on_failure(failure_result)))
        return Thenable((on_success(success_result), None))

    @classmethod
    def decorate(cls, func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorate a function to return a Thenable."""

        @functools.wraps
        def wrapper(*args: Tuple[Any], **kwargs: Dict[Any, Any]) -> Thenable:
            try:
                result = func(*args, **kwargs)
                return cls((result, None))
            except (Exception, pydantic.ValidationError) as exc:
                return cls((None, exc))

        return wrapper


ConsumerIdType = TypeVar("ConsumerIdType", bound=str)
ThenableType = TypeVar("ThenableType", bound=Thenable)
ChannelableType = NewType("ChannelableType", Channelable)
