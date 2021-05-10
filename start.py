from frankenstein_framework.main import FrameworkFranky, FakeFramework, DebugFramework
from urls import fronts
from views import routes
from wsgiref.simple_server import make_server

# application = FrameworkFranky(routes, fronts)
# application = FakeFramework(routes, fronts)
application = DebugFramework(routes, fronts)

with make_server('', 8000, application) as httpd:
    print("Запуск на порту 8000...")
    httpd.serve_forever()
