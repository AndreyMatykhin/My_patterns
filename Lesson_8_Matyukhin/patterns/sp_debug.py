from time import time


class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                print(f'debug --> Функция {self.name} выполнялась {te - ts:2.3f} ms')
                return result

            return timed

        return timeit(cls)
