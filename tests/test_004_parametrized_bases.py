from utils import raises, run_all
from stoat.core.structure import Structure
from stoat.types.ctypes import Char, Int16
from stoat.types.ctypes.params import Endianness
from stoat.core.utils import params, default


def test_parametrize_bases_params():
    class Test(Structure):
        s1: Int16 = params(endianness=Endianness.Little)
        s2: Int16 = params(endianness=Endianness.Big)

    test1 = Test()
    test1.s1 = 25185
    test1.s2 = 25185
    assert b'abba' == test1.pack()

    test2 = Test.unpack(b'BABA')
    assert 16706 == test2.s1
    assert 16961 == test2.s2


def test_parametrize_bases_default():
    class Test(Structure):
        s: Int16 = default(25185)

    test1 = Test()
    assert b'ba' == test1.pack()

    test1.s = 17238
    assert b'CV' == test1.pack()

    test2 = Test.unpack(b'WE')
    assert 22341 == test2.s


def test_parametrize_bases_default_params():
    class Test(Structure):
        s1: Int16 = default(25185), params(endianness=Endianness.Little)
        s2: Int16 = params(endianness=Endianness.Big), default(25444)

    test1 = Test()
    assert b'abcd' == test1.pack()

    test1.s1 = 25444
    test1.s2 = 25185
    assert b'dcba' == test1.pack()

    class GoodDuplicateMetadata(Structure):
        c: Char = params(a=1), params(b=2)

    with raises(Exception):  # TODO: Which Exception
        class BadDuplicateMetadata(Structure):
            c: Char = default(2), default(3)

    with raises(Exception):  # TODO: Which Exception
        class BadDuplicateMetadata2(Structure):
            c: Char = params(a=1), params(a=2)


if __name__ == '__main__':
    run_all(dir(), globals())
