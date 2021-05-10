from datetime import date
from frankenstein_framework.templ import render
from patterns.base_patterns import Engine, Logger
from patterns.struct_patterns import DecosRoutes, DecosDebug

site = Engine()
logger = Logger('main')

routes = {}


@DecosRoutes(routes=routes, url='/')
class Index:
    @DecosDebug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@DecosRoutes(routes=routes, url='/about/')
class About:
    @DecosDebug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html', data=request.get('data', None))


@DecosRoutes(routes=routes, url='/study_programs/')
class Programs:
    @DecosDebug(name='Programs')
    def __call__(self, request):
        return '200 OK', render('study_programs.html', data=request.get('data', None))


class NotFound404:
    @DecosDebug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список курсов
@DecosRoutes(routes=routes, url='/courses-list/')
class CoursesList:
    @DecosDebug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
@DecosRoutes(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @DecosDebug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except Exception:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
@DecosRoutes(routes=routes, url='/create-category/')
class CreateCategory:
    @DecosDebug(name='CreateCategory')
    def __call__(self, request):
        print(request)

        if request['method'] == 'POST':
            # метод пост
            print(request)
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
            return '200 OK', render('create_category.html', categories=categories)


# контроллер - список категорий
@DecosRoutes(routes=routes, url='/category-list/')
class CategoryList:
    @DecosDebug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


# контроллер - копировать курс
@DecosRoutes(routes=routes, url='/copy-course/')
class CopyCourse:
    @DecosDebug(name='CopyCourse')
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

            return '200 OK', render('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
