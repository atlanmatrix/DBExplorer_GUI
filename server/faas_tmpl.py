import functools
import traceback


def faas_func_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = -1
        status = 'ok'
        print('Print Log:')
        try:
            result = func(*args, **kwargs)
        except Exception:
            trace_msg = traceback.format_exc()
            print(trace_msg)
            status = 'error'
        print('\nReturn:')
        print(result)
        print(f'Status:\n{status}')
        return result
    return wrapper


#@faas_func_wrapper
#$code$


if __name__ == '__main__':
    #$name$()
    pass
