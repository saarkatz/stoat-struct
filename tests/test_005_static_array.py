from tests import raises, run_all
from stoat.Structure import Structure
from stoat.CStructure import Char, Short


def test_basic_static_array():
    class Person(Structure):
        name = Char[5]

    p1 = Person()
    p1.name = b'John\x00'
    assert b'John\x00' == p1.pack()

    assert not p1.name == b'John'
    assert not p1.name == 'John\x00'
    assert not p1.name == 5

    p1.name[4] = b'!'
    assert b'John!' == p1.pack()

    p2 = Person.unpack(b'Hello')
    assert b'l' == p2.name[3]
    assert b'e' == p2.name[-4]
    assert b'Hello' == p2.name
    assert 5 == len(p2.name)

    with raises(IndexError):
        a = p2.name[5]

    with raises(TypeError):
        p2.name = b'Text'

    with raises(TypeError):
        p2.name = 'Hello'


def test_nested_static_array():
    class String(Structure):
        length = Short
        data = Char[3]

    class Test(Structure):
        messages = String[3]

    test1 = Test()
    test1.messages[0].length = 1
    test1.messages[0].data = b'abc'
    test1.messages[1].length = 2
    test1.messages[1].data = b'def'
    test1.messages[2].length = 3
    test1.messages[2].data = b'ghi'
    assert b'\x01\x00abc\x02\x00def\x03\x00ghi' == test1.pack()

    test2 = Test.unpack(b'\x00\x01adg\x00\x02beh\x00\x03cfi')
    assert 256 == test2.messages[0].length
    assert b'adg' == test2.messages[0].data
    assert 512 == test2.messages[1].length
    assert b'beh' == test2.messages[1].data
    assert 768 == test2.messages[2].length
    assert b'cfi' == test2.messages[2].data


def test_static_multidimensional_array():
    class Test(Structure):
        matrix = Short[2][3]

    class Test2(Structure):
        cube = Short[2][3][1]

    test1 = Test()
    test1.matrix = [[1, 2, 3], [3, 4, 5]]
    assert b'\x01\x00\x02\x00\x03\x00\x03\x00\x04\x00\x05\x00' == test1.pack()

    test2 = Test.unpack(b'\x00\x01\x00\x02\x00\x03\x00\x04\x00\x08\x00\x0c')
    assert [[256, 512, 768], [1024, 2048, 3072]] == test2.matrix

    test3 = Test2()
    test3.cube = [[[1], [3], [5]], [[8], [10], [12]]]
    assert b'\x01\x00\x03\x00\x05\x00\x08\x00\x0a\x00\x0c\x00' == test3.pack()

    test4 = Test2.unpack(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c')
    assert [[[513], [1027], [1541]], [[2055], [2569], [3083]]] == test4.cube


def test_parametrized_static_array():
    class Test(Structure):
        s1 = Short[2] + '>'
        s2 = Short[1][2] + '>'

    test1 = Test()
    test1.s1 = [1, 2]
    test1.s2 = [[3, 4]]
    assert b'\x00\x01\x00\x02\x00\x03\x00\x04' == test1.pack()

    test2 = Test.unpack(b'\x01\x00\x02\x00\x03\x00\x04\x00')
    assert 256 == test2.s1[0]
    assert 512 == test2.s1[1]
    assert 768 == test2.s2[0][0]
    assert 1024 == test2.s2[0][1]


def test_reversed_array_parametrization():
    class Test(Structure):
        string = (Short + '>')[3]

    test = Test()
    test.string[0] = 258
    test.string[1] = 772
    test.string[2] = 1286
    assert b'\x01\x02\x03\x04\x05\x06' == test.pack()


if __name__ == '__main__':
    run_all(dir(), globals())
