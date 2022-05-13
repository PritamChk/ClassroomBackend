from django.urls import path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from termcolor import cprint

from classroom.views.teacher_view import (
    AnnouncementPostByTeacherViewSet,
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

teacher_sem = NestedDefaultRouter(teacher_router, "teacher", lookup="teacher")
teacher_sem.register("sem", SemesterForTeacherViewSet, basename="sem")
# TODO: implement announcement routers

teacher_subject = NestedDefaultRouter(teacher_sem, "sem", lookup="sem")
teacher_subject.register("subject", SubjectForTeacherViewSet, basename="subject")

teacher_subject_2 = NestedDefaultRouter(teacher_router, "teacher", lookup="teacher")
teacher_subject_2.register("subject", SubjectForTeacherViewSet, basename="subject")

teacher_subject_announcement = NestedDefaultRouter(
    teacher_subject_2, "subject", lookup="subject"
)
teacher_subject_announcement.register(
    "announcement", AnnouncementPostByTeacherViewSet, basename="announcement"
)

teacher_urlpatterns = []
teacher_urlpatterns += (
    teacher_router.urls
    + teacher_classrooms.urls
    + teacher_sem.urls
    + teacher_subject.urls
    + teacher_subject_announcement.urls
)

for teacher_url in teacher_urlpatterns:
    cprint(teacher_url, "yellow")
