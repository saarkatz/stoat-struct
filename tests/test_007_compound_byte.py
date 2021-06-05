from tests import raises, run_all
from stoat.core import Structure
from stoat.stypes import CompoundByte


def test_compound_byte():
    class Flags(Structure):
        flags = CompoundByte + (1, 1, 1, 1, 1, 1, 1, 1)

    f = Flags()

    assert not any(f.flags)

    f.flags[0] = True
    f.flags[2] = True
    f.flags[4] = True
    f.flags[6] = True
    f.flags[7] = True

    assert not f.flags[3]
    assert f.flags[4]
    assert b'\xab' == f.pack()

    f.flags = [not flag for flag in f.flags]
    assert b'T' == f.pack()

    f2 = Flags.unpack(b'\xff')
    assert all(f2.flags)

    class Test(Structure):
        cb1 = CompoundByte + (1, 2, 3)
        cb2 = CompoundByte + (1, 2, 3, 2)
        cb3 = CompoundByte + [4]

    t = Test()
    t.cb1[0] = 1
    t.cb1[1] = 3
    t.cb1[2] = 7
    t.cb1[3] = 3
    t.cb2 = b'\xda'
    t.cb3 = 129

    assert b'\xFF\xda\x81' == t.pack()

    with raises(TypeError):
        t.cb1 = [None, None, None, None]

    with raises(ValueError):
        t.cb1 = [3, 3, 7, 3]

    with raises(AssertionError):
        t.cb1 = [1, 2, 3]

    with raises(TypeError):
        t.cb1 = 1.373


if __name__ == '__main__':
    run_all(dir(), globals())
