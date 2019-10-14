from py_protocol import *

if __name__ == '__main__':
    class Test(Protocol):
        chars = Char[3]

    class Test2(Protocol):
        strings = Test[2]

    test = Test2()
    test.strings[0].chars = b'You'
    test.strings[1].chars = b'Roc'

    print(test.pack())
