from collections import defaultdict
from typing import Callable


class EventHandler:
    def __init__(self) -> None:
        self._registry = defaultdict(list)

    def register(self, event: str, callback: Callable):
        self._registry[event].append(callback)

    def fire(self, event: str, *args, **kwargs):
        for callback in self._registry[event]:
            callback(*args, **kwargs)
