from contextlib import ExitStack
from threading import Condition, Lock, get_ident


class RBLock:
    def __init__(self, cores, vocal=False):
        self.cores = 16
        self.locks = [Condition(Lock()) for _ in range(self.cores)]
        self.writers = []
        self.vocal = vocal

    def __call__(self, writer=False):
        if writer:
            self.writers.append(get_ident())
        return self

    def __enter__(self):
        if get_ident() in self.writers:
            self.wr_acquire()
        else:
            self.rd_acquire()

    def __exit__(self ,type, value, traceback):
        if get_ident() in self.writers:
            self.wr_release()
            self.writers.remove(get_ident())
        else:
            self.rd_release()

    def rd_acquire(self):
        core = get_ident() % self.cores
        self.locks[core].acquire()
        if self.vocal:
            print('  {} gets reader lock'.format(get_ident()))

    def rd_release(self):
        core = get_ident() % self.cores
        self.locks[core].release()
        if self.vocal:
            print('  {} releases reader lock'.format(get_ident()))

    def wr_acquire(self):
        for l in self.locks:
            l.acquire()
        if self.vocal:
            print('  {} gets writer lock'.format(get_ident()))

    def wr_release(self):
        for l in self.locks:
            l.release()
        if self.vocal:
            print('  {} releases writer lock'.format(get_ident()))

