from threading import Thread, get_ident
from random import randint

import tsqueue

class Counter:
    def __init__(self):
        self.number = 0

    def __call__(self):
        self.number += 1
        return self.number

def put(queue, value):
    queue.put(value)
    print('{}: Położyłem {} do kolejki.'.format(get_ident(), value))

def get(queue):
    try:
        value = queue.get()
        print('{}: Dostałem {} z kolejki.'.format(get_ident(), value))
    except tsqueue.Empty:
        print('{}: Kolejka jest pusta.'.format(get_ident()))

if __name__ == "__main__":
    threads = []
    queue = tsqueue.TSQueue()
    counter = Counter()

    for _ in range(20):
        if randint(0, 100) % 2 == 0:
            t = Thread(target=put, args=(queue, counter()))
        else:
            t = Thread(target=get, args=(queue, ))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(' -- fin --')
