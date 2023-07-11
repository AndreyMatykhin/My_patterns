from patterns.sap_unit_of_work import UnitOfWork
from patterns.cp_student_mapper import MapperRegistry
from patterns.bp_serializer import BaseSerializer
from patterns.bp_template import ListView, CreateView
from patterns.sp_debug import Debug
from patterns.sp_approute import AppRoute
from patterns.cp_engine import Engine
from patterns.cp_logger import Logger
from my_framework.templator import render

logger = Logger('main')
site = Engine()
site.students = MapperRegistry.get_current_mapper('student').all()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppRoute('/')
class Index:
    @Debug('Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute('/create-category/')
class CreateCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            logger.log('Создаем тему курсов')
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', objects_list=site.categories)


@AppRoute('/courses-list/')
class CoursesList:
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute('/create-course/')
class CreateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            logger.log('Создаем курс')
            data = request['data']
            name = data['name']
            type_course = 'interactive' if "type_course" in data else 'record'
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course(type_course, name, category)
                site.courses.append(course)
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))
                return '200 OK', render('create_course.html',
                                        objects_list=category.courses,
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute('/copy-course/')
class CopyCourse:
    def __call__(self, request):
        request_params = request['request_params']
        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
            return '200 OK', render('course_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute('/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute('/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student_by_course.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute('/api/')
class CourseApi:
    @Debug('CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()


@AppRoute('/contact/')
class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', object_list=[])
