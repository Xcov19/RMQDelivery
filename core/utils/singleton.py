from __future__ import annotations

from typing import Dict, Any, Tuple, Generic, TypeVar, cast


# See: https://github.com/python/mypy/issues/4236#issuecomment-416078170
class SingeltonType:
    ...


SingeltonSubType = TypeVar("SingeltonSubType", bound=SingeltonType)


class Singleton(Generic[SingeltonSubType]):
    """Singleton class for each new class type defined.

    Returns only single instance everytime it is instantiated in-memory.

    The following output is expected.

    class A(Singleton):
    ...

    a = A()


    class B(Singleton):
        ...

    b = B()

    f = A()
    assert id(a) == id(f)
    print(id(a), id(f), id(b))
    """

    _shared_state: Dict[Any, Any] = {}
    _classes: Dict[object, object] = {}

    __slots__ = (
        "__dict__",
        "_instance_class",
    )

    def __init__(self) -> None:
        self.__dict__ = self._shared_state
        self._instance_class = self._classes

    # See the issue with return annotation. est ist mit subtypes hier:
    # https://github.com/python/mypy/issues/1020
    def __new__(
        cls, *args: Tuple[Any], **kwargs: Dict[Any, Any]
    ) -> Singleton[
        SingeltonSubType
    ]:  # See why: https://github.com/python/mypy/issues/4236#issuecomment-416078170
        if not (instance := cls._classes.get(cls)):
            # You cannot do cls(*args, **kwargs)
            # instance = object.__new__(cls, *args, **kwargs)
            instance = super().__new__(cls, *args, **kwargs)
            cls._classes[cls] = instance

        __doc__ = instance.__doc__
        __module__ = instance.__module__
        # the class __init__ method won't instantiate w/o returning it's instance.
        # cast before return otherwise mypy complains of expecting object type.
        # There is no provision of Generic Subtype per se. This is the workaround.
        return cast(Singleton[SingeltonSubType], instance)
