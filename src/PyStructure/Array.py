"""
The Array class handles the containment of other structure classes into array
types.
"""
from PyStructure.BaseStructure import BaseStructure


class Array(BaseStructure):
    def __init__(self, encapsulated_cls, array_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cls = encapsulated_cls
        self.size = array_size
        if not kwargs.get('shallow', False) and isinstance(array_size, int):
            self.data = [self.cls(*args, **kwargs) for _ in range(self.size)]

    def calcsize(self, *args, **kwargs):
        size = super().calcsize()
        for value in self.data:
            size += value.calcsize()
        return size

    def pack_into(self, buffer, offset, *args, **kwargs):
        offset = super().pack_into(buffer, offset, *args, **kwargs)
        for value in self.data:
            offset = value.pack_into(buffer, offset, *args, **kwargs)
        return offset

    @classmethod
    def unpack_from(cls, buffer, offset, *args, **kwargs):
        encapsulated_cls, array_size, *args = args
        result, offset = super().unpack_from(buffer, offset, encapsulated_cls,
                                             array_size, *args, **kwargs)
        result.data = [None] * result.size
        for i in range(result.size):
            result.data[i], offset = result.cls.unpack_from(buffer, offset,
                                                            *args, **kwargs)
        return result, offset

    def _get(self, **kwargs):
        return self

    def _set(self, value, **kwargs):
        if self.size == len(value):
            for index, item in enumerate(value):
                self_assignment = self.data[index]._set(item)
                if self_assignment:
                    self.data[index] = self_assignment
        else:
            raise TypeError('value list must be of the same size ('
                            f'expected {self.size} got {len(value)})')

    def __getitem__(self, item):
        return self.data[item]._get()

    def __setitem__(self, key, value):
        self_assignment = self.data[key]._set(value)
        if self_assignment:
            self.data[key] = self_assignment

    def __eq__(self, other):
        try:
            if self.size == len(other):
                return all((v == o for v, o in zip(self.data, other)))
            else:
                return False
        except TypeError:
            return super().__eq__(other)

    @classmethod
    def array(cls, size):
        raise Exception('you are probably doing something wrong')

    @classmethod
    def param(cls, parameter):
        raise Exception('you are probably doing something wrong')

    @classmethod
    def iter(cls):
        raise TypeError('cannot unpack non-iterable Structure class {name}'
                        .format(name=cls.__name__))
