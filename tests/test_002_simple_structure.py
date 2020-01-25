from tests import run_all
from PyStructure.Structure import Structure
from PyStructure.CStructure import Char, Short


def test_simple_structure():
    class Test(Structure):
        c = Char
        s = Short

    test1 = Test()
    test1.c = b'@'
    test1.s = 9251
    assert b'@#$' == test1.pack()

    test2 = Test.unpack(b'%^&')
    assert b'%' == test2.c
    assert 9822 == test2.s

    assert 3 == test2.calcsize()

    test2.c = Char()
    assert b'\x00' == test2.c


def test_structure_inheritance():
    pass


if __name__ == '__main__':
    run_all(dir(), globals())
