from .condition import Condition


def is_int(value):
    return isinstance(value, int)


def all_range(value, bound):
    return True


def more_than(value, bound):
    return value > bound


def less_than(value, bound):
    return value < bound


def more_eq_than(value, bound):
    return value >= bound


def less_eq_than(value, bound):
    return value <= bound


def no_bound(value, bound):
    return value != bound


def only_bound(value, bound):
    return value == bound


# The no_range condition is actually illegal
def no_range(value, bound):
    return False


checks = [no_range, less_than, more_than, no_bound, only_bound, less_eq_than, more_eq_than, all_range]


class IntCondition(Condition):
    def __init__(self, anchor=0, exact=False, more=False, less=False, *, default):
        assert is_int(anchor)
        self.bound = anchor

        index = (1 if less else 0) + (2 if more else 0) + (4 if exact else 0)
        self.check = checks[index]

        assert self.validate(default)
        self._default = default

    def validate(self, value):
        return is_int(value) and self.check(value, self.bound)

    @property
    def default(self):
        return self._default
