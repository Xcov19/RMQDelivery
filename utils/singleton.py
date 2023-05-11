from typing import Dict


class Singleton:
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

    _shared_state = {}
    _classes: Dict = {}

    __slots__ = (
        "__dict__",
        "_instance_class",
    )

    def __init__(self):
        self.__dict__ = self._shared_state
        self._instance_class = self._classes

    def __new__(cls, *args, **kwargs):
        if not (instance := cls._classes.get(cls)):
            # You cannot do cls(*args, **kwargs)
            instance = cls._classes[cls] = object.__new__(cls, *args, **kwargs)

        __doc__ = instance.__doc__
        __module__ = instance.__module__
        # the class __init__ method won't instantiate w/o returning it's instance.
        return instance
