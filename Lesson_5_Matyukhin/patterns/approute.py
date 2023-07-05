routes = {}
class AppRoute:
    #

    def __init__(self, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()
