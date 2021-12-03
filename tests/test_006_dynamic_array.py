from .utils import raises, run_all
from stoat.core.structure import Structure
from stoat.types.ctypes import Char, Int16


def test_basic_dynamic_array():
    class DynamicArray(Structure):
        size: Int16
        data: Char[this.size]

    arr1 = DynamicArray()
    arr1.size = 5
    arr1.data = b'abcde'
    assert b'\x00\x05abcde' == arr1.pack()

    assert b'abcde' == arr1.data
    assert 5 == arr1.size
    assert 5 == len(arr1.data)

    arr1.size = 6
    assert b'\x00\x06abcde\x00' == arr1.pack()

    arr1.data[5] = b'!'
    assert b'\x00\x06abcde!' == arr1.pack()

    arr1.size = 2
    assert b'\x00\x02ab' == arr1.pack()

    arr2 = DynamicArray.unpack(b'\x00\x07Johnny!')
    assert b'y' == arr2.data[2]
    assert b'h' == arr2.data[-2]
    assert b'Joynnh!' == arr2.data
    assert 7 == arr2.size
    assert 7 == len(arr2.data)

    with raises(IndexError):
        a = arr2.data[7]

    with raises(TypeError):
        arr2.data = b'Text'

    with raises(TypeError):
        arr2.data = 'Froward'


def test_nested_reference_dynamic_array():
    class Number(Structure):
        value: Int16

    class Group(Structure):
        size: Number
        data: Int16[this.size.value]

    g1 = Group()
    g1.size.value = 2
    g1.data = [3, 4]
    assert b'\x00\x02\x00\x03\x00\x04' == g1.pack()

    assert [3, 4] == g1.data
    assert 2 == g1.size.value
    assert 2 == len(g1.data)

    g2 = Group.unpack(b'\x00\x03\x00\x09\x00\x51\x02\xd9')
    assert 9 == g2.data[0]
    assert 81 == g2.data[-2]
    assert [9, 81, 729] == g2.data
    assert 3 == g2.size.value


def test_nested_dynamic_array():
    class Message(Structure):
        length: Int16
        data: Char[this.length]

    class Chat(Structure):
        length: Int16
        messages: Message[this.length]

    c1 = Chat()
    c1.length = 1
    c1.messages[0].length = 2
    c1.messages[0].data = b'Hi'
    c1.length = 2
    c1.messages[1].length = 11
    c1.messages[1].data = b'How are you'
    assert b'\x00\x02\x00\x02Hi\x00\x0bHow are you' == c1.pack()

    c2 = Chat.unpack(b'\x00\x01\x00\x12Fine, how are you?')
    assert 1 == c2.length
    assert 18 == c2.messages[0].length
    assert b'Fine, how are you?' == c2.messages[0].data


def test_dynamic_multidimensional_array():
    class SquareMatrix(Structure):
        size: Int16
        data: Char[this.size][this.size]

    sm1 = SquareMatrix()
    sm1.size = 1
    sm1.data = [b'\x02']
    assert b'\x00\x01\x02' == sm1.pack()

    sm2 = SquareMatrix.unpack(b'\x00\x02\x01\x02\x03\x04')
    assert 2 == sm2.size
    assert [b'\x01\x02', b'\x03\x04'] == sm2.data

    class RectangleMatrix(Structure):
        x: Int16
        y: Int16
        data: Int16[this.x][this.y]

    rm1 = RectangleMatrix()
    rm1.x = 1
    rm1.y = 2
    rm1.data = [[3, 4]]
    assert b'\x00\x01\x00\x02\x00\x03\x00\x04' == rm1.pack()

    rm1.x = 2
    rm1.y = 1
    rm1.data = [[5], [6]]
    assert b'\x00\x02\x00\x01\x00\x05\x00\x06' == rm1.pack()

    rm2 = RectangleMatrix.unpack(
        b'\x00\x02\x00\x03\x00\x07\x00\x08\x00\x09\x00\x0a\x00\x0b\x00\x0c'
    )
    assert 2 == rm2.x
    assert 3 == rm2.y
    assert [[7, 8, 9], [10, 11, 12]] == rm2.data


def test_parametrized_dynamic_array():
    class Number(Structure):
        value: Int16

    class Test(Structure):
        size1: Int16
        size2: Int16
        s1: Int16[this.size1] = params(endianness=Endianness.Little)
        s2: Int16[this.size1][this.size2] = params(endianness=Endianness.Little)
        s3: Number[this.size2] = params(endianness=Endianness.Little)

    test1 = Test()
    test1.size1 = 1
    test1.size2 = 2
    test1.s1 = [24930]
    test1.s2 = [[25444, 25958]]
    test1.s3[0].value = 26472
    test1.s3[1].value = 26986
    assert b'\x00\x01\x00\x02abcdefghij' == test1.pack()

    test2 = Test.unpack(b'\x00\x02\x00\x01HelloWorld')
    assert 2 == test2.size1
    assert 1 == test2.size2
    assert (18533, 27756) == test2.s1
    assert [[28503], [28530]] == test2.s2
    assert 27748 == test2.s3[0].value


def test_mixed_static_dynamic_array():
    class Test1(Structure):
        size: Int16
        string: Char[2][this.size]

    test1 = Test1()
    test1.size = 3
    test1.string = ['abc', 'def']
    assert b'\x00\x03abcdef' == test1.pack()

    class Test2(Structure):
        size: Int16
        string: Char[this.size][2]

    test2 = Test2()
    test2.size = 3
    test2.string = ['gh', 'ij', 'kl']
    assert b'\x00\x03ghijkl' == test2.pack()


if __name__ == '__main__':
    run_all(dir(), globals())
