import quopri
from frankenstein_framework.request import PostRequests, GetRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 Page Not Found'


class FrameworkFranky:
    """Класс FrameworkFranky - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']
        # print('Печать environ')
        # print(path)

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        # print(f'Получаем все данные запроса {method}')
        request['method'] = method
        # print(request['method'])
        # print(environ)

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            # print(f'Отображаем данные которые пришли в байтах {data}')
            # print(type(data))
            request['data'] = data
            # print(request['data'])
            # print(request)
            print(f'Нам пришёл post-запрос: {FrameworkFranky.decode_func(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            # print(environ)
            request['request_params'] = request_params
            # print(request)
            print(f'Нам пришли GET-параметры: {request_params}')

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
            # print(path)
        else:
            view = PageNotFound404()
        print(request)

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            # print(front(request))
            front(request)
        # print(request)
        # запуск контроллера с передачей объекта request
        # print(f'Реквест {request}')
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_func(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data


# Новый вид WSGI-application, логирующий (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
class DebugFramework(FrameworkFranky):

    def __init__(self, routes_obj, fronts_obj):
        self.application = FrameworkFranky(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, environ, start_response):
        print('DEBUG MODE')
        print(environ)
        return self.application(environ, start_response)


# Новый вид WSGI-application, фейковый (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
# (на все запросы пользователя отвечает “200 OK”, “Hello from Fake”)
class FakeFramework(FrameworkFranky):

    def __init__(self, routes_obj, fronts_obj):
        self.application = FrameworkFranky(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
