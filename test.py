from py_structure import *

if __name__ == '__main__':
    class Test(Structure):
        short = Short
        char = Char

    class Test2(Structure):
        test = Test

    test2 = Test2()
    test2.test.short = 1500
    test2.test.char = b'A'

    print(test2.pack())
    test3 = Test2.unpack(b'abc')
    print(test3.test.short, test3.test.char, test3.pack())

    class Test4(Structure):
        size = -Short
        a = Char
        field = RefTest[size]
        b = Char

    test4 = Test4()
    print(test4.calcsize(), test4.pack())
    test4.size = 65
    print(test4.calcsize(), test4.pack())
    test4.field = 16
    print(test4.calcsize(), test4.pack())
    test4.size = 6
    print(test4.calcsize(), test4.pack())

    print(Test4.unpack(b'abcdef').pack())
