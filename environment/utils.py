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
