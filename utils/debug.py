import os

env = os.environ
DEBUG = env.get('DEBUG')


def i_print(*args):
    print('Info: ', end='')
    for arg in args:
        print(arg, end='')
    print()


def e_print(*args):
    print('Error: ', end='')
    for arg in args:
        print(arg, end='')
    print()


from .config import Config
config = Config.load()


def d_print(*args):
    if DEBUG:
        print('Debug: ', end='')
        for arg in args:
            print(arg, end='')
        print()
    else:
        pass
