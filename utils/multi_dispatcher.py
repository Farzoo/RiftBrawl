import typing
from typing import TypeVar, Callable, Iterable, Any, Dict, List, Tuple

TResult = TypeVar('TResult')


class MultiDispatcher(typing.Generic[TResult]):
    _MAX_INHERITANCE_DISTANCE = 2 ** 32 - 1
    _EMPTY_TUPLE = ()

    def __init__(self):
        self._registry = {}
        self._cache = {}

    def _register(self, fn):
        type_hints = typing.get_type_hints(fn)
        if 'return' in type_hints:
            type_hints.pop('return')
        types = tuple(type_hints.values())
        if self._registry.get(types) is None:
            self._registry[types] = []
        self._registry[types].append(fn)

    def dispatch(self, *args):
        actions = self.resolve(
            *map(type, args)
        )

        for action in actions:
            yield action(*args)

    def dispatch_no_collect(self, *args):
        actions = self.resolve(
            *map(type, args)
        )

        for action in actions:
            action(*args)

    def resolve(self, *types):
        actions = self._cache.get(types)
        if actions is not None:
            return actions

        best_match_keys = self._find_best_match_keys(*types)

        if len(best_match_keys) == 0:
            return self._EMPTY_TUPLE

        actions = [item for key in best_match_keys for item in self._registry[key]]

        self._cache[types] = actions

        return actions

    def _find_best_match_keys(self, *types):
        potential_keys = []
        for key in self._registry.keys():
            if len(key) != len(types):
                continue
            for (t, k) in zip(types, key):
                if not issubclass(t, k):
                    break
            else:
                potential_keys.append(key)

        if len(potential_keys) == 0:
            return potential_keys

        matches_with_distance = [(key, sum([self.get_inheritance_distance(t, k) for (t, k) in zip(types, key)])) for key
                                 in potential_keys]

        for ts1, d1 in matches_with_distance:
            for ts2, d2 in matches_with_distance:
                if len(ts1) != len(ts2):
                    continue
                if ts1 == ts2:
                    continue
                for t1, t2 in zip(ts1, ts2):
                    if not (issubclass(t1, t2) or issubclass(t2, t1)):
                        break
                else:
                    if d1 < d2:
                        matches_with_distance.remove((ts2, d2))
                    elif d2 < d1:
                        matches_with_distance.remove((ts1, d1))

        return [key for (key, distance) in matches_with_distance]

    @staticmethod
    def get_inheritance_distance(actual_type, registered_type):
        if actual_type == registered_type:
            return 0

        distance = 0
        current_type = actual_type

        stack = []

        while current_type is not None and current_type != registered_type:
            distance += 1
            stack.extend([(base, distance) for base in current_type.__bases__])
            current_type, distance = stack.pop() if len(stack) > 0 else (None, MultiDispatcher._MAX_INHERITANCE_DISTANCE)

        return distance

    class MultiDispatcherBuilder:
        def __init__(self):
            self._dispatcher = MultiDispatcher()

        def register(self, fn):
            self._dispatcher._register(fn)

        def build(self):
            return self._dispatcher
