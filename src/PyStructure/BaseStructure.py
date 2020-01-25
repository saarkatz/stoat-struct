"""
The BaseStructure class implements all structure functionality other then the
array type. This is to avoid circular import between the Structure class and
the Array class.
"""
from abc import abstractmethod
from collections import OrderedDict
from PyStructure.MetaStructure import MetaStructure


RESERVED_KEYWORDS = {'_data'}


class BaseStructure(metaclass=MetaStructure):
    def __init__(self, *args, **kwargs):
        self._data = OrderedDict()
        if kwargs.get('shallow', False):
            return
        for field, struct in self._structure.items():
            self._data[field] = struct(*args, **kwargs)

    def calcsize(self, *args, **kwargs):
        size = 0
        for data_field in self._data.values():
            size += data_field.calcsize(*args, **kwargs)
        return size

    def pack(self, *args, **kwargs):
        size = self.calcsize()
        bin_state = bytearray(size)
        self.pack_into(bin_state, 0, *args, **kwargs)
        return bytes(bin_state)

    def pack_into(self, buffer, offset, *args, **kwargs):
        for data_field in self._data.values():
            offset = data_field.pack_into(buffer, offset, *args, **kwargs)
        return offset

    @classmethod
    def unpack(cls, buffer, *args, **kwargs):
        result, _ = cls.unpack_from(buffer, 0, *args, **kwargs)
        return result

    @classmethod
    def unpack_from(cls, buffer, offset, *args, **kwargs):
        result = cls(*args, shallow=True, **kwargs)
        for field, struct in result._structure.items():
            result._data[field], offset = \
                struct.unpack_from(buffer, offset, *args, **kwargs)

        return result, offset

    def _get(self, **kwargs):
        return self

    def _set(self, value, **kwargs):
        if isinstance(value, self.__class__):
            return value
        else:
            raise TypeError('a {req} type is required (got type {got})'.format(
                req=self.__class__.__name__, got=type(value).__name__))

    @classmethod
    @abstractmethod
    def array(cls, size):
        pass

    @classmethod
    @abstractmethod
    def param(cls, parameter):
        pass

    @classmethod
    def iter(cls):
        raise TypeError('cannot unpack non-iterable Structure class {name}'
                        .format(name=cls.__name__))

    def __getattribute__(self, item):
        if item in RESERVED_KEYWORDS or item not in self._data:
            return super().__getattribute__(item)
        else:
            return self._data[item]._get()

    def __setattr__(self, key, value):
        if key in RESERVED_KEYWORDS or key not in self._data:
            super().__setattr__(key, value)
        else:
            self_assignment = self._data[key]._set(value)
            if self_assignment:
                self._data[key] = self_assignment
