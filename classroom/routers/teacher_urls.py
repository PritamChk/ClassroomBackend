from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from termcolor import cprint

from classroom.views.teacher_view import (
    ClassroomsForTeacherViewSet,
    SemesterForTeacherViewSet,
    SubjectForTeacherViewSet,
    TeacherProfileViewSet,
)

teacher_router = DefaultRouter()
teacher_router.register("teacher", TeacherProfileViewSet, basename="teacher")

teacher_classrooms = NestedDefaultRouter(teacher_router, "teacher", lookup="teacher")
teacher_classrooms.register(
    "teacher-classrooms", ClassroomsForTeacherViewSet, basename="teacher-classrooms"
)

teacher_classrooms_sem = NestedDefaultRouter(
    teacher_classrooms, "teacher-classrooms", lookup="teacher_classrooms"
)
teacher_classrooms_sem.register("sem", SemesterForTeacherViewSet, basename="sem")


teacher_subject = NestedDefaultRouter(teacher_classrooms_sem, "sem", lookup="sem")
teacher_subject.register("subject", SubjectForTeacherViewSet, basename="subject")

teacher_urlpatterns = []
teacher_urlpatterns += (
    teacher_router.urls
    + teacher_classrooms.urls
    + teacher_classrooms_sem.urls
    + teacher_subject.urls
)

for turl in teacher_urlpatterns:
    cprint(turl, "yellow")
