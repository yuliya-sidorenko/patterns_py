from frankenstein_framework.main import FrameworkFranky
from urls import routes, fronts
from wsgiref.simple_server import make_server

application = FrameworkFranky(routes, fronts)
print(routes)
print(fronts)

with make_server('', 8000, application) as httpd:
    print("Запуск на порту 8000...")
    httpd.serve_forever()
