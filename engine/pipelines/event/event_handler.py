from collections import defaultdict
from typing import Callable

from rich import print


class EventHandler:
    def __init__(self) -> None:
        self._registry = defaultdict(list)

    def register(self, event: str, callback: Callable):
        self._registry[event].append(callback)

    def fire(self, event: str, *args, **kwargs):
        for callback in self._registry.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception as ex:
                print(f"[red]Error when firing event '{event}': {ex}[/red]")

