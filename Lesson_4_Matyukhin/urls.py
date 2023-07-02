from views import Index, Contact, CreateCategory, CreateCourse, CoursesList, CopyCourse

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/create-category/': CreateCategory(),
    '/courses-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/copy-course/': CopyCourse()
}


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]
