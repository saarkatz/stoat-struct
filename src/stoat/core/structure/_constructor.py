from collections import OrderedDict

from ._reference import Reference


class Constructor:
    """Constructor is a magic dictionary

    The Constructor is used to allow the construction of structure classes while
    keeping a connection between structures that require it.
    """
    def __init__(self, metacls, name, bases):
        self.metacls = metacls
        self.name = name
        self.bases = bases
        self.fields = OrderedDict()
        self.metacls_fields = OrderedDict()

    def __setitem__(self, key, value):
        if key in self.metacls_fields:
            # TODO: What to do when a structure field is redefined?
            # This redefinition might be to a metacls field but also to
            # a structure field
            pass
        if key in self.fields:
            # TODO: What to do when a regular field is redefined?
            # Same a previous
            pass
        if isinstance(value, self.metacls):
            self.metacls_fields[key] = value
        else:
            self.fields[key] = value

    def __getitem__(self, item):
        # Assuming here that there are no collisions between fields and
        # metacls_fields
        if item in self.metacls_fields:
            # Set the field to a reference (if its not already) and
            # return it
            if not isinstance(self.metacls_fields[item], Reference):
                self.metacls_fields[item] = Reference(self.metacls_fields[item])
            return self.metacls_fields[item]
        else:
            # Otherwise attempt to return a regular field
            return self.fields[item]
