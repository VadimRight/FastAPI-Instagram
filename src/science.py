from functools import wraps
from time import time

def time_decorator(func):
    @wraps(func)
    def wrap(*args, **kw):
        time_start = time()
        result = func(*args, **kw)
        time_end = time()
        time_execution = time_end - time_start
        time_execution_milliseconds = time_execution * 1000
        print('func:%r args:[%r, %r] took: %2.4f millisec' % \
          (func.__name__, args, kw, time_execution))
        return result
    return wrap
