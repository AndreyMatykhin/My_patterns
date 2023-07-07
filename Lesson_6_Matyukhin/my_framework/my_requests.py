# get requests
class GetRequests:

    @staticmethod
    def parse_input_data(data: str):
        return {el[0]: el[1] for el in [item.split('=') for item in data.split('&')] if data}

    @staticmethod
    def get_request_params(environ):
        return GetRequests.parse_input_data(environ['QUERY_STRING'])


class PostRequests:
    @staticmethod
    def parse_input_data(data: str):
        return {el[0]: el[1] for el in [item.split('=') for item in data.split('&')] if data}

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        return env['wsgi.input'].read(content_length) if content_length > 0 else b''

    def parse_wsgi_input_data(self, data: bytes, encoding='utf-8') -> dict:
        return self.parse_input_data(data.decode(encoding) if data else '')

    def get_request_data(self, environ):
        return self.parse_wsgi_input_data(self.get_wsgi_input_data(environ))

