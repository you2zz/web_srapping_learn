from functools import wraps
import time
import datetime
import os

def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f_log:
                f_log.write(
                    f'\ncall time: {datetime.datetime.now()}; function name: {new_function.__name__}; with arguments: {args} and {kwargs}; returned: {result}')

            return result

        return new_function

    return __logger