from struct import error
from tests import raises, run_all
from stoat.core import Structure
from stoat.types import Char, Short


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

    test3 = Char.unpack(b'\x04\x02')
    assert b'\x04' == test3.pack()

    with raises(error):
        a = Short.unpack(b'\x02')


if __name__ == '__main__':
    run_all(dir(), globals())
