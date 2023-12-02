from typing import Generic, TypeVar, Callable

TArgs = TypeVar("TArgs")

class Event(Generic[TArgs]):
    def __init__(self):
        self._listeners = []

    def __call__(self, *args: TArgs, **kwargs) -> None:
        for listener in self._listeners:
            listener(*args, **kwargs)

    def __iadd__(self, listener: Callable) -> 'Event[TArgs]':
        if listener not in self._listeners:
            self._listeners.append(listener)
        return self

    def __isub__(self, listener: Callable) -> 'Event[TArgs]':
        if listener in self._listeners:
            self._listeners.remove(listener)
        return self

    def __repr__(self):
        return "Event({})".format(str(self._listeners))
