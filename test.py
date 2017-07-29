
class HogeException(Exception):
    def __init__(self):
        pass

def fuga(a):
    # something goes wrong
    if type(a) != int:
        raise HogeException()


try:
    crawl('sideboosssssk')
except UserNotFoundException as e:
    print('hoge exception raised')
