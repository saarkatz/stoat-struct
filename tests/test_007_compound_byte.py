from utils import raises, run_all
from stoat.core.structure import Structure
from stoat.types import Bits
from stoat.types.ctypes import Char


def test_compound_byte():
    class Flags(Structure):
        a: Bits = params(bits=1, skip=1)
        b: Bits = params(bits=2)
        c: Bits = params(bits=3)
        ch: Char

    f1 = Flags()
    f1.a = 1
    f1.b = 3
    f1.c = 7
    f1.ch = b'a'
    assert b'\x7ea' == f1.pack()

    f2 = Flags.unpack(b'\xaab')  # Here the last two bits will be ignored
    assert 0 == f2.a
    assert 2 == f2.b
    assert 5 == f2.c
    assert 'b' == f2.ch
    assert b'\x2a8' == f2.pack()

    with raises(OverflowError):
        f1.a = 2

    with raises(OverflowError):
        f1.b = 4


def test_cross_bytes():
    class Test(Structure):
        a: Bits = params(skip=4, bits=8)

    t1 = Test.unpack(b'\x09\xa0')
    t2 = Test.unpack(b'\xf9\xaf')

    assert t1.a == t2.a
    assert t1.pack() == t2.pack()


def test_bits_array():
    class Test(Structure):
        a: Bits[4] = params(skip=1, bits=2)

    t = Test.unpack(b'e2a5')

    assert 3 == t.a[0]
    assert 0 == t.a[1]
    assert 1 == t.a[2]
    assert 2 == t.a[3]
    assert 2 == t.a[-1]
    assert b'60a0' == t.pack()

    with raises(IndexError):
        t.a[4] = 1


if __name__ == '__main__':
    run_all(dir(), globals())
