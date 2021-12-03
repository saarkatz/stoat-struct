from .utils import run_all
from stoat.core.structure import Structure
from stoat.types.ctypes import Char, Int16
from stoat.types.ctypes.params import Endianness
from stoat.core.utils import params


def test_parametrize_structure():
    class Test(Structure):
        c: Char
        s: Int16 = params(endianness=param.endianness)

    test1 = Test(endianness=Endianness.Big)
    test1.c = 'a'
    test1.s = 17238
    assert b'aCV' == test1.pack()

    test2 = Test(endianness=Endianness.Little)
    test1.c = 'b'
    test2.s = 17238
    assert b'bVC' == test2.pack()


def test_parametrize_nested_structure():
    class Inner(Structure):
        c: Char
        s: Int16 = params(endianness=param.endi)

    class Test(Structure):
        i1: Inner = params(endi=param.paparam)
        i2: Inner = params(endi=Endianness.Big)

    test = Test(paparam=Endianness.Little)
    test.i1.c = 'a'
    test.i1.s = 17238
    test.i1.c = 'b'
    test.i1.s = 17238
    assert b'aVCbCV' == test.pack()


if __name__ == '__main__':
    run_all(dir(), globals())
