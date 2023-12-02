from typing import Generic, Callable, TypeVar

T = TypeVar("T")


class LazyClassField(Generic[T]):

    def __init__(self, fn: Callable[[], T]):
        self._fn = fn
        self._value = None

    def __get__(self, instance, owner) -> T:
        if self._value is None:
            self._value = self._fn()
        return self._value

    @staticmethod
    def create(fn: Callable[[], T]) -> 'LazyClassField[T]':
        return LazyClassField(fn)
