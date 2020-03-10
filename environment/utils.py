from typing import Dict, Any


class DelayedUpdateMixin:
    def __init__(self):
        self._next_values = {}

    def delay_update(self, field: str, value):
        self._next_values[field] = value

    def update(self):
        for field, value in self._next_values.items():
            try:
                setattr(self, field, value)
            except AttributeError as e:
                raise e


class MultipleParentsInheritor:
    def __init__(self, kwargs: Dict[type, Dict[str, Any]]):
        for parent_class in self.__class__.__bases__:
            if hasattr(parent_class, '__init__') and parent_class is not MultipleParentsInheritor:
                parent_class.__init__(self, **kwargs[parent_class])
