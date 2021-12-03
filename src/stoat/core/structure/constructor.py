from collections import OrderedDict

from .ref import This


class Constructor:
    def __init__(self, name):
        self.special = {'this': This()}
        self.fields = OrderedDict({'__name__': name})

    def __getitem__(self, item):
        if item in self.special:
            return self.fields.get(item, self.special[item])
        return self.fields[item]

    def __setitem__(self, item, value):
        self.fields[item] = value

    def __delitem__(self, item):
        del self.fields[item]
