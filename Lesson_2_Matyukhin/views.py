from my_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', object_list=[])


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html',object_list=[])
