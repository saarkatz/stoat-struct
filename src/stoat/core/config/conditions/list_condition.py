from .condition import Condition


class ListCondition(Condition):
    def __init__(self, iterator, *, default):
        self.values = tuple(iterator)
        assert self.validate(default)
        self._default = default

    def validate(self, value):
        return value in self.values

    @property
    def default(self):
        return self._default
