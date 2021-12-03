from struct import error

from utils import raises, run_all
from stoat.core.structure import Structure
from stoat.types.ctypes import Char, Int16


def test_simple_structure():
    class Test(Structure):
        c: Char
        s: Int16

    test1 = Test()
    test1.c = b'@'
    test1.s = 9251
    assert b'@$#' == test1.pack()

    test2 = Test.unpack(b'%&^')
    assert '%' == test2.c
    assert 9822 == test2.s

    assert 3 == test2.calcsize()

    test2.c = Char()
    assert '\x00' == test2.c

    test3 = Char.unpack(b'\x04\x02')
    assert b'\x04' == test3.pack()

    with raises(error):
        a = Int16.unpack(b'\x02')


if __name__ == '__main__':
    run_all(dir(), globals())
