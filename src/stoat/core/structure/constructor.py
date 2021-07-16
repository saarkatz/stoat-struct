from collections import OrderedDict

from .context import ForwardRef
from .context.reference import get_target


class Constructor:
    """Constructor is a magic dictionary

    The Constructor is used to allow the construction of structure classes while
    keeping a connection between structures that require it.
    """
    def __init__(self, metacls, name, bases, ref_vars_func):
        self.metacls = metacls
        self.ref_vars_func = ref_vars_func

        self.fields = OrderedDict()

    def __setitem__(self, key, value):
        self.setitem(key, value)

    def __getitem__(self, item):
        return self.getitem(item)

    # TODO: __delitem__ for completeness
    def __delitem__(self, key):
        del self.fields[key]

    def setitem(self, key, value):
        if isinstance(value, ForwardRef):
            value = get_target(value)

        if key in self.fields:
            del self.fields[key]
        self.fields[key] = value

    def getitem(self, item):
        if isinstance(self.fields[item], self.metacls):
            return ForwardRef(
                self.metacls,
                self.fields[item],
                item,
                self.ref_vars_func,
            )
        else:
            return self.fields[item]

    def get(self, item, default):
        return self.fields.get(item, default)
