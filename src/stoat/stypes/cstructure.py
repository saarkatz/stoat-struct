import ctypes
import struct
from enum import Enum, unique
from collections import namedtuple

from stoat.core import Structure
from stoat.core.config.conditions import ListCondition
from stoat.auxiliary.config_builder import ConfigBuilder, EnumItem


CTypeTuple = namedtuple("CType", ["name", "fmt", "type"])


class ConfigParams:
    type = "type"
    endianness = "endianness"


class Endianness(Enum):
    Little = '<'
    Big = '>'


class CType(Enum):
    Byte = CTypeTuple("byte", "c", ctypes.c_char)  # byte (8 bit)
    Char = CTypeTuple("char", "c", ctypes.c_char)  # char (8 bit)
    Short = CTypeTuple("short", "h", ctypes.c_int16)  # short (16 bit)
    Int = CTypeTuple("int", "i", ctypes.c_int32)  # int (32 bit)
    Long = CTypeTuple("long", "q", ctypes.c_int64)  # long long (64 bit)


# Distinguish between number types and character types
CharType = [CType.Char]
NumType = [t for t in CType if t not in CharType]


Config = ConfigBuilder([
    EnumItem(ConfigParams.type, "Type", CType),
    EnumItem(ConfigParams.endianness, "Endianness", Endianness),
])


class BaseCStructure(Structure):
    _config = {
        ConfigParams.type: ListCondition([None], default=None),
        ConfigParams.endianness: ListCondition([None], default=None),
    }

    def __init__(self, _parent=None):
        super().__init__(_parent=_parent)
        self.fmt = (
            self._config.get(ConfigParams.endianness).value
            + self._config.get(ConfigParams.type).value.fmt
        )
        self.data = self.type()

    @property
    def type(self):
        return self._config.get(ConfigParams.type).value.type

    def calcsize(self):
        size = super().calcsize()
        return size + struct.calcsize(self.fmt)

    def pack_into(self, buffer, offset):
        offset = super().pack_into(buffer, offset)
        struct.pack_into(self.fmt, buffer, offset, self.data.value)
        return offset + struct.calcsize(self.fmt)

    @classmethod
    def unpack_from(cls, buffer, offset, *args, **kwargs):
        result, offset = super().unpack_from(buffer, offset, *args, **kwargs)
        value = struct.unpack_from(result.fmt, buffer, offset)[0]
        assignment = result._set(value)
        if not assignment:
            assignment = result
        return assignment, offset + struct.calcsize(result.fmt)

    def _get(self, **kwargs):
        return self.data.value

    def _set(self, value, **kwargs):
        try:
            self.data.value = value
        except TypeError as e:
            try:
                return super()._set(value)
            except TypeError:
                raise e

    def __eq__(self, other):
        if isinstance(other, BaseCStructure):
            return self.data.value == other.data.value
        elif isinstance(other, self.type):
            return self.data == other
        else:
            return self.data.value == other


class BaseCharType(BaseCStructure):
    _config = {
        ConfigParams.type: ListCondition(CharType, default=CType.Char),
        ConfigParams.endianness: ListCondition(Endianness, default=Endianness.Little),
    }

    def __eq__(self, other):
        if isinstance(other, BaseCStructure):
            return self.data.value == other.data.value
        elif isinstance(other, self.type):
            return self.data == other
        else:
            return ord(self.data.value) == other


class BaseNumType(BaseCStructure):
    _config = {
        ConfigParams.type: ListCondition(NumType, default=CType.Byte),
        ConfigParams.endianness: ListCondition(Endianness, default=Endianness.Little),
    }


Char = BaseCharType
Short = BaseNumType < Config.Type.Short.bake()
Int = BaseNumType < Config.Type.Int.bake()
Long = BaseNumType < Config.Type.Long.bake()


if __name__ == '__main__':
    print(Config.Type.Char.Endianness.Big.bake())