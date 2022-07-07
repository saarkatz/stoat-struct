from abc import abstractmethod
import struct

from ...core.structure import Structure
from .params import Endianness


class BaseCStructure(Structure):
    def __init__(self, default=0, params=None):
        super().__init__()
        self.endianness = params.get('endianness', Endianness.Big) if params else Endianness.Big

        if isinstance(default, self.__class__):
            default = default.data.value
        self.data = self.type(default)
        self._fmt = self.endianness.value + self.fmtchar

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def fmtchar(self):
        pass

    @property
    def fmt(self):
        return self._fmt

    def calcsize(self):
        size = super().calcsize()
        return size + struct.calcsize(self.fmt)

    def pack_into(self, buffer, offset):
        offset = super().pack_into(buffer, offset)
        struct.pack_into(self.fmt, buffer, offset, self.data.value)
        return offset + struct.calcsize(self.fmt)

    @classmethod
    def unpack_from(cls, buffer, offset, kwargs=None):
        result, offset = super().unpack_from(buffer, offset, kwargs)
        value = struct.unpack_from(result.fmt, buffer, offset)[0]
        result.setter(value)
        return result, offset + struct.calcsize(result.fmt)

    def getter(self):
        return self.data.value

    def setter(self, value):
        if isinstance(value, self.__class__):
            self.data = value.data
        elif isinstance(value, self.type.__class__):
            self.data = value
        else:
            try:
                self.data.value = value
            except TypeError as e:
                try:
                    super().setter(value)
                except TypeError:
                    raise e

    def __eq__(self, other):
        if isinstance(other, BaseCStructure):
            return self.data.value == other.data.value
        elif isinstance(other, self.type):
            return self.data == other
        else:
            return self.data.value == other



