from quopri import decodestring
from .my_requests import GetRequests, PostRequests


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
        request['method'] = environ['REQUEST_METHOD']
        if request['method'] == 'POST':
            request['data'] = MyFramework.decode_value(PostRequests().get_request_data(environ))
        if request['method'] == 'GET':
            request['request_params'] = MyFramework.decode_value(
                GetRequests().parse_input_data(environ['QUERY_STRING']))

        # front controller
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
