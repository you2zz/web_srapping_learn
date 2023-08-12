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
                f_log.write(f'\ncall time: {datetime.datetime.now()}; function name: {new_function.__name__}; with arguments: {args} and {kwargs}; returned: {result}')

            return result

        return new_function

    return __logger


def log_clean(path):
    def __log_clean(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            f = open(path, 'w', encoding='utf-8')
            f.write(f'\ncall time: {datetime.datetime.now()}; function name: {new_function.__name__}. Файл {path} очищен. Ведется запись текущей сессии.')
            f.close()
            result = old_function(*args, **kwargs)
            return result

        return new_function

    return __log_clean


def with_attempts(max_attempts=3, timeout=0.1):
    def _with_attempts(any_function):
        @wraps(any_function)
        def new_function(*args, **kwargs):
            for i in range(1, max_attempts + 1):
                result = any_function(*args, **kwargs)
                if result[1] == 200:
                    # print(f'Успешное подключение к {result[2]}')
                    break
                else:
                    print(f'Не удалось подключиться к {result[2]}')
                    time.sleep(timeout)
            return result

        return new_function

    return _with_attempts


def with_attempts_data(path, max_attempts=3, timeout=0.1):
    def _with_attempts_data(any_function):
        @wraps(any_function)
        def new_function(*args, **kwargs):
            for i in range(1, max_attempts + 1):
                result = any_function(*args, **kwargs)
                if result[0] is not None:
                    with open(path, 'a', encoding='utf-8') as f_log:
                        f_log.write(f'\ncall time: {datetime.datetime.now()}; function name: {new_function.__name__}; Получено описание вакансии со страницы: {result[1]}')
                    break
                else:
                    with open(path, 'a', encoding='utf-8') as f_log:
                        f_log.write(f'\ncall time: {datetime.datetime.now()}; function name: {new_function.__name__}; Не получены данные со страницы: {result[1]}')
                    time.sleep(timeout)
            return result

        return new_function

    return _with_attempts_data
