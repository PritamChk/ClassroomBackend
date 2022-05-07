from django.urls import path, include
from termcolor import cprint
# from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views.student_view import user_category

from .views.student_view import StudentProfileViewSet,ClassroomForStudentViewSet

# from .views.student_view import DynamicRetriveUser

student_router = DefaultRouter()
student_router.register("student", StudentProfileViewSet, "student")

# student_classroom_router = NestedDefaultRouter(student_router,'student',lookup = 'student')
# student_classroom_router.register('classroom',ClassroomForStudentViewSet,basename='student-classroom')

classroom_router = DefaultRouter()
classroom_router.register('classroom',ClassroomForStudentViewSet,'classroom')

urlpatterns = [path("user-type/<uuid:id>", user_category, name="user-category")]

urlpatterns += student_router.urls +classroom_router.urls

for url in urlpatterns:
    cprint(url,'green')