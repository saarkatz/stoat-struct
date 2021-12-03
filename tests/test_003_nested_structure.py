from utils import run_all
from stoat.core.structure import Structure
from stoat.types.ctypes import Char, Int16


def test_structure_in_structure():
    class CharStruct(Structure):
        c1: Char
        c2: Char

    class ShortStruct(Structure):
        s1: Int16
        s2: Int16

    class Test(Structure):
        s: Int16
        cs: CharStruct
        ss: ShortStruct
        c: Char

    test1 = Test()
    test1.s = 8574
    test1.cs.c1 = b'@'
    test1.cs.c2 = b'#'
    test1.ss.s1 = 9508
    test1.ss.s2 = 9822
    test1.c = b'*'
    assert b'!~@#%$&^*' == test1.pack()

    c = Char.unpack(b'a')
    cs = CharStruct()
    cs.c1 = b'b'
    cs.c2 = b'c'
    test1.c = c
    test1.cs = cs
    assert b'!~bc%$&^a' == test1.pack()


if __name__ == '__main__':
    run_all(dir(), globals())
