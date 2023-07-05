from wsgiref.simple_server import make_server

from patterns.approute import routes
from urls import fronts
from my_framework.main import MyFramework

application = MyFramework(routes, fronts)
with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
