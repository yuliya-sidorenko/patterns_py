from time import time


# Cтруктурный паттерн - Декоратор
class DecosRoutes:
    # сохраняются данные-маршруты\urls
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    # декоратор
    def __call__(self, cls_name):
        self.routes[self.url] = cls_name()


# структурный паттерн - Декоратор
class DecosDebug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls_name):
        # декоратор
        # это вспомогательная функция будет декорировать каждый отдельный метод класса, замеряя время его выполнения

        def timeit(method):
            def time_check(*args, **kw):
                time_start = time()
                result = method(*args, **kw)
                time_end = time()
                delta = time_end - time_start

                print(f'DEBUG: Метод "{self.name}" выполнялся {delta:2.2f} ms')
                return result

            return time_check

        return timeit(cls_name)
