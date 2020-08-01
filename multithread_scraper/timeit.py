from time import time

def timeit(func):
    def timedFunc(*args, **kwargs):
        startTime = time()
        func(*args, **kwargs)
        endTime = time()
        elapsed_time = endTime - startTime
        elapsed_time = round(elapsed_time, 2)
        print(f'{func.__name__} executed in {elapsed_time}s')
    return timedFunc