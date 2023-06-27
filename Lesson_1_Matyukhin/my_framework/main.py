class PageNotFound404:
    def __call__(self, request):
        return '404 NOT FOUND', '<h1>404 Not Found</h1>'


class MyFramework:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if path[-1] != '/':
            path += '/'
        # page controller
        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()
        request = {}
        # front controller
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
