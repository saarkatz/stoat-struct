from struct import error

from .utils import raises, run_all
from stoat.core.structure import Structure
from stoat.types.ctypes import Char, Int16


def test_simple_structure():
    class Test(Structure):
        c: Char
        s: Int16

    test1 = Test()
    test1.c = b'*'
    test1.s = 10281
    assert b'*()' == test1.pack()
    assert 3 == test1.calcsize()

    test2 = Test({'c': b'@', 's': 9251})
    assert b'@$#' == test2.pack()

    c = Char(101)
    test3 = Test({'c': c, 's': 1})
    assert b'e\x00\x01' == test3.pack()

    test4 = Test(test3)
    assert b'e\x00\x01' == test4.pack()
    test4.s = 2
    assert b'e\x00\x02' == test4.pack()
    assert b'e\x00\x01' == test3.pack()

    test5 = Test.unpack(b'%&^')
    assert '%' == test5.c
    assert 9822 == test5.s

    test5.c = Char(1)
    assert '\x01' == test5.c

    test6 = Char.unpack(b'\x04\x02')
    assert b'\x04' == test6.pack()

    with raises(error):
        a = Int16.unpack(b'\x02')


if __name__ == '__main__':
    run_all(dir(), globals())
