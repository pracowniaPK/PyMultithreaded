from threading import Thread, get_ident
from random import randint

from rblock import RBLock


class Resource:
    def __init__(self, initial):
        self.value = initial

    def write(self, new):
        self.value = new

    def read(self):
        return self.value

def write(lock, resource, new):
    with lock(writer=True):
        resource.write(new)
        print('I\'m {}. I write {}'.format(get_ident(), new))

def read(lock, resource):
    with lock():
        print('I\'m {}. I read {}'.format(get_ident(), resource.read()))


if __name__ == "__main__":

    lock = RBLock(8, vocal=False)
    resource = Resource(0)
    threads = []

    for _ in range(20):
        if randint(0, 1000) % 4 == 0:
            t = Thread(target=write, args=(lock, resource, randint(1, 99)))
        else:
            t = Thread(target=read, args=(lock, resource))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print('-- fin --')
