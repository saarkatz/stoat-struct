from tests import raises, run_all
from PyStructure.Structure import Structure
from PyStructure.CStructure import Char, Short


def test_parametrize_bases():
    class Test(Structure):
        s1 = Short+'<'
        s2 = Short+'>'

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
        i1 = Internal+'>'
        i2 = Internal+'<'

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
