from collections import namedtuple
from enum import Enum
import struct

from ...core.configuration.conditions import ListCondition
from ...core.structure import Structure


CTypeTuple = namedtuple("CType", ["name", "fmt", "type"])


class ConfigParams:
    type = "Type"
    endianness = "Endianness"


class Endianness(Enum):
    Little = '<'
    Big = '>'


class BaseCStructure(Structure):
    __config__ = {
        ConfigParams.type: ListCondition([None], default=None),
        ConfigParams.endianness: ListCondition([None], default=None),
    }

    def __init__(self, _parent=None):
        super().__init__()
        self.fmt = (
            self.__config__.get(ConfigParams.endianness).value
            + self.__config__.get(ConfigParams.type).value.fmt
        )
        self.data = self.type()

    @property
    def type(self):
        return self.__config__.get(ConfigParams.type).value.type

    def calcsize(self):
        size = super().calcsize()
        return size + struct.calcsize(self.fmt)

    def pack_into(self, buffer, offset):
        offset = super().pack_into(buffer, offset)
        struct.pack_into(self.fmt, buffer, offset, self.data.value)
        return offset + struct.calcsize(self.fmt)

    @classmethod
    def unpack_from(cls, buffer, offset):
        result, offset = super().unpack_from(buffer, offset)
        value = struct.unpack_from(result.fmt, buffer, offset)[0]
        result.setter(value)
        return result, offset + struct.calcsize(result.fmt)

    def getter(self):
        return self.data.value

    def setter(self, value):
        if isinstance(value, self.__class__):
            self.data = value.data
        elif isinstance(value, self.type):
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

a = 1