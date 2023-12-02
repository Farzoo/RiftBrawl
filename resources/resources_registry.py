from typing import Generic, TypeVar, Dict

K = TypeVar("K")
V = TypeVar("V")


class ResourcesRegistry(Generic[K, V]):

    def __init__(self):
        self._resources = {}

    def __getitem__(self, item: K) -> V:
        return self._resources[item]

    def __setitem__(self, key: K, value: V):
        self._resources[key] = value

    def keys(self):
        return self._resources.keys()

    class ResourceRegistryBuilder(Generic[K, V]):
        def __init__(self):
            self._registry = ResourcesRegistry[K, V]()

        def register(self, name: K, resource: V):
            self._registry._resources[name] = resource
            return self

        def build(self) -> 'ResourcesRegistry[K, V]':
            registry = self._registry
            self._registry = ResourcesRegistry[K, V]()
            return registry
