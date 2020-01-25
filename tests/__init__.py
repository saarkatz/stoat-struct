from pytest import raises
from colorama import Fore, Style


def run_all(dir, globals):
    keys = [key for key in dir if 'test' in key]
    tests = [globals[key] for key in keys if callable(globals[key])]

    for key, test in zip(keys, tests):
        print(key, end='...')
        try:
            test()
        except:
            print(' ' + Fore.RED + 'fail' + Style.RESET_ALL)
            raise
        else:
            print(' ' + Fore.GREEN + 'success' + Style.RESET_ALL)
