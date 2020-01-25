import ctypes
import struct as Struct
from PyStructure.Structure import Structure


class BaseCStructure(Structure):
    def __init__(self, ctype, fmt, endianness, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctype = ctype
        self.fmt = endianness + fmt
        self.data = ctype()

    def calcsize(self, *args, **kwargs):
        size = super().calcsize(*args, **kwargs)
        return size + Struct.calcsize(self.fmt)

    def pack_into(self, buffer, offset, *args, **kwargs):
        offset = super().pack_into(buffer, offset, *args, **kwargs)
        Struct.pack_into(self.fmt, buffer, offset, self.data.value)
        return offset + Struct.calcsize(self.fmt)

    @classmethod
    def unpack_from(cls, buffer, offset, *args, **kwargs):
        result, offset = super().unpack_from(buffer, offset, *args, **kwargs)
        value = Struct.unpack_from(result.fmt, buffer, offset)[0]
        assignment = result._set(value)
        if not assignment:
            assignment = result
        return assignment, offset + Struct.calcsize(result.fmt)

    def _get(self, **kwargs):
        return self.data.value

    def _set(self, value, **kwargs):
        error = None
        try:
            self.data.value = value
        except TypeError as e:
            error = e
        if error:
            try:
                return super()._set(value, **kwargs)
            except TypeError:
                raise error

    def __eq__(self, other):
        return (self.data.value == other
                or self.data == other)


class Char(BaseCStructure):
    def __init__(self, endianness='', *args, **kwargs):
        super().__init__(ctypes.c_char, 'c', endianness, *args, **kwargs)

    def __eq__(self, other):
        return (super().__eq__(other)
                or ord(self.data.value) == other)


class Short(BaseCStructure):
    def __init__(self, endianness='', *args, **kwargs):
        super().__init__(ctypes.c_short, 'h', endianness, *args, **kwargs)


class Int(BaseCStructure):
    def __init__(self, endianness='', *args, **kwargs):
        super().__init__(ctypes.c_int, 'i', endianness, *args, **kwargs)
