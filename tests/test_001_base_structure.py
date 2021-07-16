from tests import raises, run_all
from stoat.types.ctypes import Char, Short


def test_char_structure():
    c = Char()
    c.setter(b'@')
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

    # with raises(TypeError):
    #     c.setter('@')


def test_short_structure():
    s = Short()
    s.setter(14)
    assert b'\x0e\x00' == s.pack()
    assert 14 == s.getter()

    s.setter(-1)
    assert b'\xff\xff' == s.pack()
    assert -1 == s.getter()

    s.setter(32768)
    assert b'\x00\x80' == s.pack()


if __name__ == '__main__':
    run_all(dir(), globals())
