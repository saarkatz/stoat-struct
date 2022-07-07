from .utils import raises, run_all
from stoat.types.ctypes import Char, Int16


def test_char_structure():
    c = Char(b'@')
    assert b'@' == c.pack()
    assert '@' == c.getter()

    c.setter(bytearray(b'a'))
    assert b'a' == c.pack()
    assert 'a' == c.getter()

    c.setter(70)
    assert b'F' == c.pack()
    assert 'F' == c.getter()

    c.setter('H')
    assert b'H' == c.pack()
    assert 'H' == c.getter()

    # with raises(OverflowError):
    #     c.setter(256)

    with raises(TypeError):
        c.setter(256)


def test_short_structure():
    s = Int16(14)
    assert b'\x00\x0e' == s.pack()
    assert 14 == s.getter()

    s.setter(-1)
    assert b'\xff\xff' == s.pack()
    assert -1 == s.getter()

    s.setter(-32768)
    assert b'\x80\x00' == s.pack()

    # with raises(OverflowError):
    #     s.setter(32768)


if __name__ == '__main__':
    run_all(dir(), globals())
