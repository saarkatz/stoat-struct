from abc import abstractmethod
from collections import OrderedDict, namedtuple

from .meta import Meta


Instance = namedtuple(
    'Instance',
    [
        'data',
    ]
)


class Base(metaclass=Meta):
    """Base is base class for the Structure class and Array class

    This class is required to prevent circular import between Structure
    and Array.
    """
    def __init__(self, **kwargs):
        params = kwargs.get('params', {})  # TODO: default behaviour should be to pass the params to any requiring child
        shape, metadata = self.__blueprint__
        instance = Instance(data=OrderedDict())

        for key, struct in shape.items():
            instance.data[key] = struct(**metadata[key])

        self.__instance__ = instance

    def calcsize(self):
        size = 0
        for field in self.__instance__.data.values():
            size += field.calcsize()
        return size

    def pack(self):
        size = self.calcsize()
        bin_state = bytearray(size)
        self.pack_into(bin_state, 0)
        return bytes(bin_state)

    def pack_into(self, buffer, offset):
        for field in self.__instance__.data.values():
            offset = field.pack_into(buffer, offset)
        return offset

    @classmethod
    def unpack(cls, buffer):
        result, _ = cls.unpack_from(buffer, 0)
        return result

    @classmethod
    def unpack_from(cls, buffer, offset, kwargs=None):
        result = cls(**kwargs) if kwargs else cls()
        shape, metadata = result.__blueprint__

        for key, struct in shape.items():
            result.__instance__.data[key], offset = (
                struct.unpack_from(buffer, offset, metadata[key])
            )
        return result, offset

    def getter(self):
        return self

    def setter(self, value):
        if isinstance(value, self.__class__):
            for key in self.__blueprint__.shape.keys():
                setattr(self, key, getattr(value, key))
        else:
            raise TypeError(
                f'a {self.__class__.__name__} type is required (got type'
                f' {type(value).__name__})'
            )

    @classmethod
    @abstractmethod
    def array(cls, size):
        pass
