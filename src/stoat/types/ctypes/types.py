import ctypes

from ...core.structure.meta import Meta
from .base_ctype import BaseCStructure


def make_ctype(name, ctype, fmtchar):
    return Meta.dynamic(name, (BaseCStructure,), {
        'type': property(lambda self: ctype),
        'fmtchar': property(lambda self: fmtchar),
    }, {})


Int8 = make_ctype('Int8', ctypes.c_int8, 'c')
Int16 = make_ctype('Int16', ctypes.c_int16, 'h')
Int32 = make_ctype('Int32', ctypes.c_int32, 'i')
Int64 = make_ctype('Int64', ctypes.c_int64, 'q')


class Char(BaseCStructure):
    @property
    def type(self):
        return ctypes.c_char

    @property
    def fmtchar(self):
        return 'c'

    def getter(self):
        return super().getter().decode("utf-8")

    def setter(self, value):
        super().setter(ord(value) if isinstance(value, str) else value)

