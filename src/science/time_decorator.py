from functools import wraps
from time import time

analysis_data = []
analysis_data_output = []

def time_decorator(func):
    @wraps(func)
    async def wrapped(*args, **kw):
        time_start = time()
        result = await func(*args, **kw)
        time_end = time()
        time_execution = time_end - time_start
        time_execution_milliseconds = time_execution * 1000
        analysis_data.append(time_execution_milliseconds)
        global analysis_data_output
        analysis_data_output = analysis_data
        print(analysis_data_output)
        print('func:%r args:[%r, %r] took: %2.4f millisec' % \
        (func.__name__, args, kw, time_execution_milliseconds))
        return result
    return wrapped

print(analysis_data_output)
