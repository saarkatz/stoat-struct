"""
The Array class handles the containment of other structure classes into array
types.
"""
from stoat.core.base_structure import BaseStructure


class ConstantSize:
    def __init__(self, value):
        self.value = value


class ReferenceSize:
    def __init__(self, path, source):
        while isinstance(source, Array):
            source = source._parent
        target = source
        for subfield in path.split('.'):
            target = target._data[subfield]
        self.reference = target

    @property
    def value(self):
        return self.reference._get()


class Array(BaseStructure):
    def __init__(self, encapsulated_cls, array_size, *args, parent=None,
                 **kwargs):
        super().__init__(*args, parent=parent, **kwargs)
        self.cls = encapsulated_cls
        self._size = self.init_size(array_size)
        self.data = []
        self.args = args
        self.kwargs = kwargs

    def init_size(self, size):
        if isinstance(size, int):
            return ConstantSize(size)
        elif isinstance(size, str):
            return ReferenceSize(size, self._parent)
        else:
            raise ValueError('Size is set to an inappropriate type '
                             '({size})'.format(size=type(size)))

    def resize_data(self):
        if len(self.data) < self.size:
            self.data.extend((self.cls(*self.args, parent=self, **self.kwargs)
                              for _ in range(self.size - len(self.data))))
        elif len(self.data) > self.size:
            self.data = self.data[:self.size]

    @property
    def size(self):
        return self._size.value

    def calcsize(self, *args, **kwargs):
        self.resize_data()
        size = super().calcsize()
        for value in self.data:
            size += value.calcsize()
        return size

    def pack_into(self, buffer, offset, *args, **kwargs):
        offset = super().pack_into(buffer, offset, *args, **kwargs)
        self.resize_data()
        for value in self.data:
            offset = value.pack_into(buffer, offset, *args, **kwargs)
        return offset

    @classmethod
    def unpack_from(cls, buffer, offset, *args, parent=None, **kwargs):
        encapsulated_cls, array_size, *args = args
        result, offset = super().unpack_from(buffer, offset, encapsulated_cls,
                                             array_size, *args, parent=parent,
                                             **kwargs)
        result.data = [None] * result.size
        for i in range(result.size):
            result.data[i], offset = result.cls.unpack_from(buffer, offset,
                                                            *args,
                                                            parent=result,
                                                            **kwargs)
        return result, offset

    def _get(self, **kwargs):
        return self

    def _set(self, value, **kwargs):
        self.resize_data()
        if self.size == len(value):
            for index, item in enumerate(value):
                self_assignment = self.data[index]._set(item)
                if self_assignment:
                    self.data[index] = self_assignment
        else:
            raise TypeError('value list must be of the same size ('
                            f'expected {self.size} got {len(value)})')

    def __getitem__(self, item):
        self.resize_data()
        return self.data[item]._get()

    def __setitem__(self, key, value):
        self.resize_data()
        self_assignment = self.data[key]._set(value)
        if self_assignment:
            self.data[key] = self_assignment

    def __eq__(self, other):
        self.resize_data()
        try:
            if self.size == len(other):
                return all((v == o for v, o in zip(self.data, other)))
            else:
                return False
        except TypeError:
            return super().__eq__(other)

    def __len__(self):
        return self.size

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
