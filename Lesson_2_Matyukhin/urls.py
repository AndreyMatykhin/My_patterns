from views import Index, Contact

routes = {
    '/': Index(),
    '/contact/': Contact(),
}


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]