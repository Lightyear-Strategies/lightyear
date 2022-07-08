import time # for time tracker

def timethis(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('[*] Execution time: {} seconds.'.format(end-start))
        return result
    return wrapper