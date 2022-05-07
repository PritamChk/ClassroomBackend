from django.urls import path, include
from termcolor import cprint

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .views.student_view import SemesterForStudentViewSet, user_category

from .views.student_view import StudentProfileViewSet, ClassroomForStudentViewSet


student_router = DefaultRouter()
student_router.register("student", StudentProfileViewSet, "student")


classroom_router = DefaultRouter()
classroom_router.register("classroom", ClassroomForStudentViewSet, "classroom")

classroom_sems_router = NestedDefaultRouter(
    classroom_router, "classroom", lookup="classroom"
)
classroom_sems_router.register(
    "semester", SemesterForStudentViewSet, basename="sem"
)

urlpatterns = [path("user-type/<uuid:id>", user_category, name="user-category")]

urlpatterns += student_router.urls + classroom_router.urls + classroom_sems_router.urls

for url in urlpatterns:
    cprint(url, "green")
