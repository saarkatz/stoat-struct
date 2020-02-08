
"""
The TypeFactory class is used to encapsulate all Structure classes for the
purpose of containing the data required for the initialization of the structure.
"""
from PyStructure.BaseTypeFactory import BaseTypeFactory
from PyStructure.Array import Array


class TypeFactory(BaseTypeFactory):
    def __init__(self, encapsulated_cls, *args, **kwargs):
        self.cls = encapsulated_cls
        self.args = list(args)
        self.kwargs = kwargs

    def unpack_from(self, buffer, offset, *args, **kwargs):
        return self.cls.unpack_from(buffer, offset, *self.args, *args,
                                    **self.kwargs, **kwargs)

    def __getitem__(self, size):
        if issubclass(self.cls, Array):
            self.args[0] = TypeFactory(Array, self.args[0], size)
            return self
        else:
            return TypeFactory(Array, self, size)

    def __add__(self, parameter):
        self.args.append(parameter)
        return self

    def __iter__(self):
        return self.cls.iter(*self.args, **self.kwargs)

    def __call__(self, *args, **kwargs):
        return self.cls(*self.args, *args, **self.kwargs, **kwargs)
