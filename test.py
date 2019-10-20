from py_protocol import *

if __name__ == '__main__':
    class Test(Protocol):
        chars = -Short[2]+'<'

    class Test2(Protocol):
        strings = -Test[2]

    test = Test2()
    test.strings[0].chars[0] = 25
    test.strings[1].chars[0] = 150

    print(test.pack())
