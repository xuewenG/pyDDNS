from utils.config import Config

config = Config.load()


def i_print(*args):
    print('Info: ', end='')
    for arg in args:
        print(arg, end='')
    print()


def d_print(*args):
    if config['DEBUG']:
        print('Debug: ', end='')
        for arg in args:
            print(arg, end='')
        print()
    else:
        pass


def e_print(*args):
    print('Error: ', end='')
    for arg in args:
        print(arg, end='')
    print()
