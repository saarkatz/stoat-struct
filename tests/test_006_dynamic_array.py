from tests import raises, run_all
from PyStructure.Structure import Structure
from PyStructure.CStructure import Char, Short


def test_basic_dynamic_array():
    class DynamicArray(Structure):
        size = Short
        data = Char['size']

    arr1 = DynamicArray()
    arr1.size = 5
    arr1.data = b'abcde'
    assert b'\x05\x00abcde' == arr1.pack()

    assert b'abcde' == arr1.data
    assert 5 == arr1.size
    assert 5 == arr1.data.size

    arr1.size = 6
    assert b'\x06\x00abcde\x00' == arr1.pack()

    arr1.data[5] = b'!'
    assert b'\x06\x00abcde!' == arr1.pack()

    arr1.size = 2
    assert b'\x02\x00ab' == arr1.pack()

    arr2 = DynamicArray.unpack(b'\x07\x00Johnny!')
    assert b'h' == arr2.data[2]
    assert b'y' == arr2.data[-2]
    assert b'Johnny!' == arr2.data
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
        value = Short

    class Group(Structure):
        size = Number
        data = Short['size.value']

    g1 = Group()
    g1.size.value = 2
    g1.data = [3, 4]
    assert b'\x02\x00\x03\x00\x04\x00' == g1.pack()

    assert [3, 4] == g1.data
    assert 2 == g1.size.value
    assert 2 == g1.data.size

    g2 = Group.unpack(b'\x03\x00\x09\x00\x51\x00\xd9\x02')
    assert 9 == g2.data[0]
    assert 81 == g2.data[-2]
    assert [9, 81, 729] == g2.data
    assert 3 == g2.size.value


def test_nested_dynamic_array():
    class Message(Structure):
        length = Short
        data = Char['length']

    class Chat(Structure):
        length = Short
        messages = Message['length']

    c1 = Chat()
    c1.length = 1
    c1.messages[0].length = 2
    c1.messages[0].data = b'Hi'
    c1.length = 2
    c1.messages[1].length = 11
    c1.messages[1].data = b'How are you'
    assert b'\x02\x00\x02\x00Hi\x0b\x00How are you' == c1.pack()

    c2 = Chat.unpack(b'\x01\x00\x12\x00Fine, how are you?')
    assert 1 == c2.length
    assert 18 == c2.messages[0].length
    assert b'Fine, how are you?' == c2.messages[0].data


def test_dynamic_multidimensional_array():
    class SquareMatrix(Structure):
        size = Short
        data = Char['size']['size']

    sm1 = SquareMatrix()
    sm1.size = 1
    sm1.data = [b'\x02']
    assert b'\x01\x00\x02' == sm1.pack()

    sm2 = SquareMatrix.unpack(b'\x02\x00\x01\x02\x03\x04')
    assert 2 == sm2.size
    assert [b'\x01\x02', b'\x03\x04'] == sm2.data

    class RectangleMatrix(Structure):
        x = Short
        y = Short
        data = Short['x']['y']

    rm1 = RectangleMatrix()
    rm1.x = 1
    rm1.y = 2
    rm1.data = [[3, 4]]
    assert b'\x01\x00\x02\x00\x03\x00\x04\x00' == rm1.pack()

    rm1.x = 2
    rm1.y = 1
    rm1.data = [[5], [6]]
    assert b'\x02\x00\x01\x00\x05\x00\x06\x00' == rm1.pack()

    rm2 = RectangleMatrix.unpack(
        b'\x02\x00\x03\x00\x07\x00\x08\x00\x09\x00\x0a\x00\x0b\x00\x0c\x00')
    assert 2 == rm2.x
    assert 3 == rm2.y
    assert [[7, 8, 9], [10, 11, 12]] == rm2.data


def test_parametrized_dynamic_array():
    class Number(Structure):
        value = Short

    class Test(Structure):
        size1 = Short
        size2 = Short
        s1 = Short['size1'] + '>'
        s2 = Short['size1']['size2'] + '>'
        s3 = Number['size2'] + '>'

    test1 = Test()
    test1.size1 = 1
    test1.size2 = 2
    test1.s1 = [24930]
    test1.s2 = [[25444, 25958]]
    test1.s3[0].value = 26472
    test1.s3[1].value = 26986
    assert b'\x01\x00\x02\x00abcdefghij' == test1.pack()

    test2 = Test.unpack(b'\x02\x00\x01\x00HelloWorld')
    assert 2 == test2.size1
    assert 1 == test2.size2
    assert (18533, 27756) == test2.s1
    assert [[28503], [28530]] == test2.s2
    assert 27748 == test2.s3[0].value


def test_reversed_dynamic_array_parametrization():
    class Test(Structure):
        size = Short
        string = (Short + '>')['size']

    test = Test()
    test.size = 3
    test.string[0] = 258
    test.string[1] = 772
    test.string[2] = 1286
    assert b'\x03\x00\x01\x02\x03\x04\x05\x06' == test.pack()


if __name__ == '__main__':
    run_all(dir(), globals())
