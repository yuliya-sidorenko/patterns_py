class GetRequests:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            print(f'Данные из QUERY_STRING get-запроса: {data}')
            # Разделяем параметры по знаку &
            params = data.split('&')
            print(params)
            for item in params:
                # Разделяем ключ и значение по знаку =
                key, val = item.split('=')
                result[key] = val
                print(result)
        return result

    @staticmethod
    def get_request_params(environ):
        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        print(f'Получаем параметры запроса {query_string}')
        # превращаем параметры в словарь
        request_params = GetRequests.parse_input_data(query_string)
        print(request_params)
        return request_params


# post requests
class PostRequests:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            # Разделяем параметры по знаку &
            params = data.split('&')
            print(params)
            for item in params:
                # Разделяем ключ и значение по знаку =
                key, val = item.split('=')
                result[key] = val
                print(result)
        return result

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        # получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # print(env.get(''))
        print(f'Получаем длину тела всего сообщения в байтах: {content_length_data}')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        print(content_length)
        # считываем данные, если они есть
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        print(data)
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            print(f'декодируем данные - {data}')
            data_str = data.decode(encoding='utf-8')
            print(data_str)
            # собираем их в словарь
            result = self.parse_input_data(data_str)
            print(result)
        return result

    def get_request_params(self, environ):
        # получаем данные из словаря
        print(f'получаем данные из словаря {environ} вызывается функция get_wsgi_input_data ')
        data = self.get_wsgi_input_data(environ)

        # превращаем данные в словарь
        data = self.parse_wsgi_input_data(data)
        print(f'превращаем данные - {data} в словарь')
        return data
