from tests import raises, run_all
from stoat.core import Structure
from stoat.stypes import Char, Short, Config


def test_parametrize_bases():
    class Test(Structure):
        s1 = Short < Config.Endianness.Little
        s2 = Short < Config.Endianness.Big

    test1 = Test()
    test1.s1 = 25185
    test1.s2 = 25185
    assert b'abba' == test1.pack()

    test2 = Test.unpack(b'BABA')
    assert 16706 == test2.s1
    assert 16961 == test2.s2


def test_parametrize_nested():
    class Internal(Structure):
        c = Char
        s = Short

    class Test(Structure):
        i1 = Internal < Config.Endianness.Big
        i2 = Internal < Config.Endianness.Little

    test1 = Test()
    test1.i1.c = b'a'
    test1.i1.s = 17238
    test1.i2.c = b'b'
    test1.i2.s = 17238
    assert b'aCVbVC' == test1.pack()

    test2 = Test.unpack(b'qWErWE')
    assert 22341 == test2.i1.s
    assert 17751 == test2.i2.s


if __name__ == '__main__':
    run_all(dir(), globals())
