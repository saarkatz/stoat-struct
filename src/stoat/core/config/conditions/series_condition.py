from .condition import Condition


class SeriesCondition(Condition):
    def __init__(self, start, step, *, default):
        # Assert that all the values are integers
        for value in [start, step]:
            if not isinstance(value, int):
                raise TypeError(
                    "'{}' object cannot be interpreted as an integer".format(
                        value.__class__.__name__))

        if step == 0:
            raise ValueError("SeriesCondition arg 3 must not be zero")
        elif step > 0:
            self.sign = 1
        else:
            self.sign = -1

        self.start, self.step = start, step
        assert self.validate(default)
        self._default = default

    def validate(self, value):
        return self.sign * self.start <= self.sign * value and (value - self.start) % self.step == 0

    @property
    def default(self):
        return self._default
