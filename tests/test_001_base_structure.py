from tests import raises, run_all
from PyStructure.CStructure import Char, Short


def test_char_structure():
    c = Char()
    c._set(b'@')
    assert b'@' == c.pack()
    assert b'@' == c._get()

    c._set(bytearray(b'a'))
    assert b'a' == c.pack()
    assert b'a' == c._get()

    c._set(70)
    assert b'F' == c.pack()
    assert b'F' == c._get()

    with raises(TypeError):
        c._set('@')


def test_short_structure():
    s = Short()
    s._set(14)
    assert b'\x0e\x00' == s.pack()
    assert 14 == s._get()

    s._set(-1)
    assert b'\xff\xff' == s.pack()
    assert -1 == s._get()

    s._set(32768)
    assert b'\x00\x80' == s.pack()


if __name__ == '__main__':
    run_all(dir(), globals())
