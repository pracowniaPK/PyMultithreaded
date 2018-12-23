import multiprocessing as mp
import math
import time

X0 = 1
X1 = 40
STEPS = int(10**5.5)
PRCS = 8

def f(x):
    return 3*x**3 + math.cos(7*x) + math.log(2*x)
    # return x

def stats(func):
    def wrapper(*args, **kwargs):
        try:
            print("{}:".format(args[0].__name__))
        except:
            print("{}:".format(func.__name__))
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print("dt = {}".format(t2-t1))
    return wrapper

def integral1(f, x0, x1, steps, sum):
    dx = (x1-x0) / steps
    for i in range(steps):
        sum.value += f(x0+dx*i)*dx

def integral2(f, x0, x1, steps, sum):
    dx = (x1-x0) / steps
    for i in range(steps):
        s = f(x0+dx*i)*dx
        with sum.get_lock():
            sum.value += s

def integral3(f, x0, x1, steps, sum):
    dx = (x1-x0) / steps
    s = 0
    for i in range(steps):
        s += f(x0+dx*i)*dx
    with sum.get_lock():
        sum.value += s

@stats
def case(integral):
    sum1 = mp.Value("d", 0)
    dx = (X1-X0) / PRCS
    processes = [mp.Process(target=integral, 
        args=(f, X0+i*dx, X0+i*dx+dx, STEPS, sum1))
        for i in range(PRCS)]
    
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print("result = {}".format(sum1.value))
    

if __name__ == "__main__":
    print("Liczba procesów: {}\nLiczba przedziałów całkowania: {}\n"
        .format(PRCS, STEPS))
    case(integral1)
    print("W pierwszym przypadku otrzymujemy dziwaczny wynik ponieważ procesy odczytują i zapisują współdzieloną zmienną bez synchronizacji.\n")
    case(integral2)
    print("W drugim przypadku dostajemy poprawny wynik, niestety konieczność operowania na jednej zmiennej przez wysztkie procesy dramatycznie obniża wydajność.\n")
    case(integral3)
    print("Trzeci przypadek pozwala prowadzić obliczenia w sposób ciągły, bez konieczności oczekiwania na zwolnienie zamka przez inne procesy przy każdym obrocie pętli.")
