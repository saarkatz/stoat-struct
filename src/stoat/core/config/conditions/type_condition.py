from .condition import Condition


class TypeCondition(Condition):
    def __init__(self, type=None, nullable=True, *, default=None):
        self.type = type
        self.nullable = nullable

        assert self.validate(default)
        self._default = default

    def validate(self, value):
        if value is not None:
            return isinstance(value, self.type)
        elif self.nullable:
            return True
        else:
            return False

    @property
    def default(self):
        return self._default
