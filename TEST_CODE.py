def inner():
    print('func')

def test(func):
    func()

test(inner)